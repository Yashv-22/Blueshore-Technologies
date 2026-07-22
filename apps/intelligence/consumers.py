import json
import uuid
import re
import urllib.request
from django.conf import settings
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from apps.intelligence.models import VisitorSession, VisitorTimelineEvent, SessionReplayFrame
from apps.chatbot.models import ChatConversation, ChatMessage
from apps.contact.models import ContactRequest
import google.generativeai as genai

# Helper to get geolocation
def get_location_by_ip(ip):
    if not ip or ip in ('127.0.0.1', 'localhost') or ip.startswith('192.168.') or ip.startswith('10.'):
        return 'India', 'Delhi NCR'
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,city"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            if data.get('status') == 'success':
                return data.get('country', 'Unknown'), data.get('city', 'Unknown')
    except Exception as e:
        print(f"GeoIP Error: {e}")
    return 'Unknown', 'Unknown'

# Helper to generate AI chatbot replies (Gemini)
def generate_ai_chat_reply(user_message, history_messages):
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    
    # Import prompt templates & fallbacks from existing chatbot app
    from apps.chatbot.views import SYSTEM_PROMPT, generate_fallback_reply
    from apps.chatbot.utils import sanitize_lead_jargon, API_KEY_PATTERNS
    
    if not api_key:
        return generate_fallback_reply(user_message)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        contents = []
        for msg in history_messages:
            role = 'model' if msg.sender in ('AI', 'Admin') else 'user'
            contents.append({
                'role': role,
                'parts': [{'text': msg.text}]
            })
            
        # Add last message
        contents.append({
            'role': 'user',
            'parts': [{'text': user_message}]
        })
        
        response = model.generate_content(
            contents=contents,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=600,
            )
        )
        reply = response.text
        # Redact keys
        for pattern in API_KEY_PATTERNS:
            reply = pattern.sub('[REDACTED API KEY]', reply)
        reply = sanitize_lead_jargon(reply)
        return reply
    except Exception as e:
        print(f"Gemini AI Chat Error: {e}")
        return generate_fallback_reply(user_message)

# Helper to generate suggestion quick replies for admin
def generate_admin_suggestions(user_message, conversation):
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return ["Would you like to schedule a strategy call?", "Let me fetch that information for you.", "What is your project budget?"]
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        history = ChatMessage.objects.filter(conversation=conversation).order_by('created_at')
        history_str = "\n".join([f"{msg.sender}: {msg.text}" for msg in history[:10]])
        
        prompt = f"""
You are assisting an admin agent who is chatting with a customer.
Generate exactly 3 suggested replies for the admin to click and send.
Keep suggestions short, conversational, helpful, and context-aware.
Return ONLY a valid JSON array of 3 strings. Example: ["Hello! Yes we do.", "We can schedule a call.", "What is your budget?"]
Do not add markdown format or backticks.

Context history:
{history_str}
Visitor last message: {user_message}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```'):
            text = re.sub(r'^```(?:json)?\n|```$', '', text, flags=re.MULTILINE).strip()
        suggestions = json.loads(text)
        if isinstance(suggestions, list) and len(suggestions) >= 3:
            return suggestions[:3]
    except Exception as e:
        print(f"Suggestions Generation Error: {e}")
    return ["Would you like to schedule a strategy call?", "Let me fetch that information for you.", "What is your project budget?"]


class VisitorConsumer(WebsocketConsumer):
    def connect(self):
        self.session_id = None
        self.accept()

    def disconnect(self, close_code):
        if self.session_id:
            # Set visitor offline in DB
            VisitorSession.objects.filter(session_id=self.session_id).update(
                is_online=False,
                last_activity=timezone.now()
            )
            # Notify admins visitor went offline
            async_to_sync(self.channel_layer.group_send)(
                "admin_dashboard",
                {
                    "type": "visitor_offline",
                    "session_id": self.session_id
                }
            )
            # Remove from groups
            async_to_sync(self.channel_layer.group_discard)(f"visitor_{self.session_id}", self.channel_name)

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            return
            
        msg_type = data.get("type")
        
        if msg_type == "init":
            self.session_id = data.get("session_id")
            visitor_id = data.get("visitor_id")
            if not self.session_id or not visitor_id:
                return
                
            # Add to visitor's group
            async_to_sync(self.channel_layer.group_add)(f"visitor_{self.session_id}", self.channel_name)
            
            # Extract metadata
            ip = self.scope.get("client", [None])[0] or "127.0.0.1"
            ua = dict(self.scope.get("headers", [])).get(b"user-agent", b"").decode()
            
            # Resolve geolocation
            country, city = get_location_by_ip(ip)
            
            # Get or create visitor session
            session, created = VisitorSession.objects.get_or_create(
                session_id=self.session_id,
                defaults={
                    "visitor_id": visitor_id,
                    "ip_address": ip,
                    "user_agent": ua,
                    "browser": data.get("browser", "Unknown"),
                    "device": data.get("device", "Desktop"),
                    "os": data.get("os", "Unknown"),
                    "screen_size": data.get("screen_size", "Unknown"),
                    "country": country,
                    "city": city,
                    "referrer": data.get("referrer", ""),
                    "first_visit": data.get("first_visit", True),
                    "is_returning": data.get("is_returning", False),
                    "current_url": data.get("current_url", ""),
                    "current_page_title": data.get("page_title", "Home"),
                    "is_online": True,
                    "chat_status": "No Chat"
                }
            )
            if not created:
                session.is_online = True
                session.last_activity = timezone.now()
                session.save()
                
            # Create a timeline event for arrival
            VisitorTimelineEvent.objects.create(
                session=session,
                event_type="Arrival",
                description=f"Visitor arrived on site from {session.referrer or 'Direct'}"
            )
            
            # Broadcast arrival to admins
            self.broadcast_session_update(session)
            
        elif msg_type == "page_update":
            if not self.session_id:
                return
            current_url = data.get("current_url", "")
            page_title = data.get("page_title", "Home")
            prev_url = data.get("previous_url", "")
            
            session = VisitorSession.objects.filter(session_id=self.session_id).first()
            if session:
                session.previous_url = session.current_url
                session.current_url = current_url
                session.current_page_title = page_title
                session.last_activity = timezone.now()
                session.save()
                
                # Check for High Intent Page changes (Contact / Pricing)
                score_changed = False
                if "pricing" in current_url.lower() and "pricing" not in session.scored_milestones:
                    session.scored_milestones.append("pricing")
                    session.lead_score += 20
                    score_changed = True
                if "contact" in current_url.lower() and "contact" not in session.scored_milestones:
                    session.scored_milestones.append("contact")
                    session.lead_score += 25
                    score_changed = True
                
                if score_changed:
                    session.save()
                
                # Create timeline event
                VisitorTimelineEvent.objects.create(
                    session=session,
                    event_type="PageView",
                    description=f"Navigated to {page_title}"
                )
                
                self.broadcast_session_update(session)
                
        elif msg_type == "scroll_update":
            if not self.session_id:
                return
            scroll_pct = int(data.get("scroll_percentage", 0))
            section = data.get("section", "Hero")
            
            session = VisitorSession.objects.filter(session_id=self.session_id).first()
            if session:
                session.scroll_percentage = scroll_pct
                if scroll_pct > session.max_scroll:
                    session.max_scroll = scroll_pct
                session.current_section = section
                session.last_activity = timezone.now()
                session.save()
                
                # If section changed, record timeline event
                last_event = session.timeline_events.filter(event_type="SectionView").last()
                if not last_event or last_event.details.get("section") != section:
                    VisitorTimelineEvent.objects.create(
                        session=session,
                        event_type="SectionView",
                        description=f"Scrolled to section: {section}",
                        details={"section": section, "scroll_percentage": scroll_pct}
                    )
                
                self.broadcast_session_update(session)
                
        elif msg_type == "idle_update":
            if not self.session_id:
                return
            is_idle = data.get("is_idle", False)
            session = VisitorSession.objects.filter(session_id=self.session_id).first()
            if session:
                session.is_idle = is_idle
                session.last_activity = timezone.now()
                session.save()
                
                VisitorTimelineEvent.objects.create(
                    session=session,
                    event_type="Status",
                    description="Visitor went idle" if is_idle else "Visitor resumed activity"
                )
                
                self.broadcast_session_update(session)
                
        elif msg_type == "typing_status":
            if not self.session_id:
                return
            is_typing = data.get("is_typing", False)
            # Broadcast typing status to admins
            async_to_sync(self.channel_layer.group_send)(
                "admin_dashboard",
                {
                    "type": "visitor_typing",
                    "session_id": self.session_id,
                    "is_typing": is_typing
                }
            )

        elif msg_type == "replay_frame":
            if not self.session_id:
                return
            frames = data.get("frames", [])
            if not frames:
                return
                
            session = VisitorSession.objects.filter(session_id=self.session_id).first()
            if session:
                # Save replay chunk to database
                SessionReplayFrame.objects.create(
                    session=session,
                    events_data=json.dumps(frames)
                )
                # Broadcast live replay cursor actions to listening admins
                async_to_sync(self.channel_layer.group_send)(
                    "admin_dashboard",
                    {
                        "type": "live_replay_data",
                        "session_id": self.session_id,
                        "frames": frames
                    }
                )

        elif msg_type == "chat_message":
            if not self.session_id:
                return
            text = data.get("text", "").strip()
            if not text:
                return
                
            session = VisitorSession.objects.filter(session_id=self.session_id).first()
            if not session:
                return
                
            # Get or create chatbot conversation
            conversation, _ = ChatConversation.objects.get_or_create(
                session_id=self.session_id
            )
            
            # Map CRM lead if available
            if session.lead and not conversation.lead:
                conversation.lead = session.lead
                conversation.save()
                
            # Increment lead score on starting chat
            score_changed = False
            if "opened_chat" not in session.scored_milestones:
                session.scored_milestones.append("opened_chat")
                session.lead_score += 30
                session.chat_status = "Active"
                score_changed = True
                
            if score_changed:
                session.save()
                
            if session.chat_mode in ('AI', 'Hybrid'):
                # In AI/Hybrid mode, the HTTP streaming endpoint handles database saving,
                # lead extraction, and AI response generation.
                # Here, we only broadcast the user message to the admin dashboard in real-time
                # and record a timeline event.
                temp_id = "temp_" + str(uuid.uuid4())
                async_to_sync(self.channel_layer.group_send)(
                    "admin_dashboard",
                    {
                        "type": "new_chat_message",
                        "session_id": self.session_id,
                        "message": {
                            "id": temp_id,
                            "sender": "User",
                            "text": text,
                            "created_at": timezone.now().strftime('%I:%M %p')
                        }
                    }
                )
                
                # Create Timeline Event
                VisitorTimelineEvent.objects.create(
                    session=session,
                    event_type="ChatMessage",
                    description=f"Visitor: {text[:40]}...",
                    details={"sender": "User"}
                )
                self.broadcast_session_update(session)
            else:
                # Human takeover mode: WebSocket handles database saving & admin routing
                user_msg = ChatMessage.objects.create(
                    conversation=conversation,
                    sender='User',
                    text=text
                )
                
                from apps.chatbot.views import extract_lead_info
                extract_lead_info(text, conversation)
                if conversation.lead and not session.lead:
                    session.lead = conversation.lead
                    session.lead_score += 50
                    session.save()
                    
                VisitorTimelineEvent.objects.create(
                    session=session,
                    event_type="ChatMessage",
                    description=f"Visitor: {text[:40]}...",
                    details={"message_id": str(user_msg.id), "sender": "User"}
                )
                
                async_to_sync(self.channel_layer.group_send)(
                    "admin_dashboard",
                    {
                        "type": "new_chat_message",
                        "session_id": self.session_id,
                        "message": {
                            "id": str(user_msg.id),
                            "sender": "User",
                            "text": text,
                            "created_at": user_msg.created_at.strftime('%I:%M %p')
                        }
                    }
                )
                self.broadcast_session_update(session)
            
            # Generate AI Suggestions for admin (always generated in background for live view support)
            suggestions = generate_admin_suggestions(text, conversation)
            async_to_sync(self.channel_layer.group_send)(
                "admin_dashboard",
                {
                    "type": "ai_suggestions",
                    "session_id": self.session_id,
                    "suggestions": suggestions
                }
            )

    def broadcast_session_update(self, session):
        # Broadcast full session state to admins
        async_to_sync(self.channel_layer.group_send)(
            "admin_dashboard",
            {
                "type": "session_update",
                "session": {
                    "session_id": session.session_id,
                    "visitor_id": session.visitor_id,
                    "ip_address": session.ip_address,
                    "browser": session.browser,
                    "device": session.device,
                    "os": session.os,
                    "screen_size": session.screen_size,
                    "country": session.country,
                    "city": session.city,
                    "referrer": session.referrer,
                    "first_visit": session.first_visit,
                    "is_returning": session.is_returning,
                    "current_url": session.current_url,
                    "page_title": session.current_page_title,
                    "scroll_percentage": session.scroll_percentage,
                    "max_scroll": session.max_scroll,
                    "current_section": session.current_section,
                    "active_tab": session.active_tab,
                    "is_idle": session.is_idle,
                    "is_online": session.is_online,
                    "lead_score": session.lead_score,
                    "chat_mode": session.chat_mode,
                    "chat_status": session.chat_status,
                    "lead_name": session.lead.name if session.lead else (conversation_lead_name(session.session_id)),
                    "last_activity": session.last_activity.strftime('%I:%M %p'),
                    "conversion_probability": session.conversion_probability,
                    "recommended_service": session.recommended_service,
                    "estimated_budget": session.estimated_budget,
                    "urgency": session.urgency
                }
            }
        )

    # Group message handlers
    def session_mode_changed(self, event):
        self.send(json.dumps({
            "type": "mode_change",
            "chat_mode": event["chat_mode"]
        }))

    def admin_message_received(self, event):
        self.send(json.dumps({
            "type": "chat_message",
            "message": event["message"]
        }))

    def admin_typing_status(self, event):
        self.send(json.dumps({
            "type": "typing_status",
            "sender": "Admin",
            "is_typing": event["is_typing"]
        }))


def conversation_lead_name(session_id):
    conv = ChatConversation.objects.filter(session_id=session_id).first()
    return conv.lead.name if conv and conv.lead else None


class AdminConsumer(WebsocketConsumer):
    def connect(self):
        # Authenticate staff users
        self.user = self.scope.get("user")
        if not self.user or not self.user.is_staff:
            self.close()
            return
            
        async_to_sync(self.channel_layer.group_add)("admin_dashboard", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("admin_dashboard", self.channel_name)

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            return
            
        msg_type = data.get("type")
        
        if msg_type == "takeover_action":
            session_id = data.get("session_id")
            chat_mode = data.get("chat_mode")  # AI, Human, Hybrid
            if not session_id or chat_mode not in ('AI', 'Human', 'Hybrid'):
                return
                
            session = VisitorSession.objects.filter(session_id=session_id).first()
            if session:
                session.chat_mode = chat_mode
                if chat_mode in ('Human', 'Hybrid'):
                    session.chat_status = "Active"
                session.save()
                
                # Notify visitor connection about mode change
                async_to_sync(self.channel_layer.group_send)(
                    f"visitor_{session_id}",
                    {
                        "type": "session_mode_changed",
                        "chat_mode": chat_mode
                    }
                )
                # Save timeline event
                VisitorTimelineEvent.objects.create(
                    session=session,
                    event_type="Takeover",
                    description=f"Chat mode changed to {chat_mode} by {self.user.username}"
                )
                # Broadcast session update back to all admins
                self.broadcast_session_update(session)
                
        elif msg_type == "admin_message":
            session_id = data.get("session_id")
            text = data.get("text", "").strip()
            if not session_id or not text:
                return
                
            session = VisitorSession.objects.filter(session_id=session_id).first()
            if not session:
                return
                
            # Get conversation
            conversation, _ = ChatConversation.objects.get_or_create(session_id=session_id)
            
            # Save message to DB
            msg = ChatMessage.objects.create(
                conversation=conversation,
                sender='Admin',
                text=text
            )
            
            # Timeline Event
            VisitorTimelineEvent.objects.create(
                session=session,
                event_type="ChatMessage",
                description=f"Admin ({self.user.username}): {text[:40]}...",
                details={"message_id": str(msg.id), "sender": "Admin"}
            )
            
            # Send message to visitor
            async_to_sync(self.channel_layer.group_send)(
                f"visitor_{session_id}",
                {
                    "type": "admin_message_received",
                    "message": {
                        "id": str(msg.id),
                        "sender": "Admin",
                        "text": text,
                        "created_at": msg.created_at.strftime('%I:%M %p')
                    }
                }
            )
            
            # Broadcast to all admins (to sync other open chat consoles)
            async_to_sync(self.channel_layer.group_send)(
                "admin_dashboard",
                {
                    "type": "new_chat_message",
                    "session_id": session_id,
                    "message": {
                        "id": str(msg.id),
                        "sender": "Admin",
                        "text": text,
                        "created_at": msg.created_at.strftime('%I:%M %p')
                    }
                }
            )
            
        elif msg_type == "typing_status":
            session_id = data.get("session_id")
            is_typing = data.get("is_typing", False)
            if not session_id:
                return
            # Send typing status to visitor
            async_to_sync(self.channel_layer.group_send)(
                f"visitor_{session_id}",
                {
                    "type": "admin_typing_status",
                    "is_typing": is_typing
                }
            )
            
        elif msg_type == "proactive_message":
            session_id = data.get("session_id")
            text = data.get("text", "").strip()
            if not session_id or not text:
                return
            
            session = VisitorSession.objects.filter(session_id=session_id).first()
            if not session:
                return
                
            conversation, _ = ChatConversation.objects.get_or_create(session_id=session_id)
            
            # Save message as Admin
            msg = ChatMessage.objects.create(
                conversation=conversation,
                sender='Admin',
                text=text
            )
            
            VisitorTimelineEvent.objects.create(
                session=session,
                event_type="ProactiveMessage",
                description=f"Proactive message: {text[:40]}..."
            )
            
            # Send to visitor (with special tag to pop-open widget if not open)
            async_to_sync(self.channel_layer.group_send)(
                f"visitor_{session_id}",
                {
                    "type": "admin_message_received",
                    "message": {
                        "id": str(msg.id),
                        "sender": "Admin",
                        "text": text,
                        "created_at": msg.created_at.strftime('%I:%M %p'),
                        "proactive": True
                    }
                }
            )
            
            # Broadcast to admins
            async_to_sync(self.channel_layer.group_send)(
                "admin_dashboard",
                {
                    "type": "new_chat_message",
                    "session_id": session_id,
                    "message": {
                        "id": str(msg.id),
                        "sender": "Admin",
                        "text": text,
                        "created_at": msg.created_at.strftime('%I:%M %p')
                    }
                }
            )

    # Broadcast session update back to all admins
    def broadcast_session_update(self, session):
        async_to_sync(self.channel_layer.group_send)(
            "admin_dashboard",
            {
                "type": "session_update",
                "session": {
                    "session_id": session.session_id,
                    "visitor_id": session.visitor_id,
                    "ip_address": session.ip_address,
                    "browser": session.browser,
                    "device": session.device,
                    "os": session.os,
                    "screen_size": session.screen_size,
                    "country": session.country,
                    "city": session.city,
                    "referrer": session.referrer,
                    "first_visit": session.first_visit,
                    "is_returning": session.is_returning,
                    "current_url": session.current_url,
                    "page_title": session.current_page_title,
                    "scroll_percentage": session.scroll_percentage,
                    "max_scroll": session.max_scroll,
                    "current_section": session.current_section,
                    "active_tab": session.active_tab,
                    "is_idle": session.is_idle,
                    "is_online": session.is_online,
                    "lead_score": session.lead_score,
                    "chat_mode": session.chat_mode,
                    "chat_status": session.chat_status,
                    "lead_name": session.lead.name if session.lead else (conversation_lead_name(session.session_id)),
                    "last_activity": session.last_activity.strftime('%I:%M %p'),
                    "conversion_probability": session.conversion_probability,
                    "recommended_service": session.recommended_service,
                    "estimated_budget": session.estimated_budget,
                    "urgency": session.urgency
                }
            }
        )

    # Methods handling group messages from visitor activity
    def session_update(self, event):
        self.send(json.dumps(event))

    def visitor_offline(self, event):
        self.send(json.dumps(event))

    def visitor_typing(self, event):
        self.send(json.dumps(event))

    def live_replay_data(self, event):
        self.send(json.dumps(event))

    def new_chat_message(self, event):
        self.send(json.dumps(event))

    def ai_suggestions(self, event):
        self.send(json.dumps(event))

import time
import json
import re
import google.generativeai as genai
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from apps.chatbot.models import ChatConversation, ChatMessage
from apps.contact.models import ContactRequest

SYSTEM_PROMPT = """You are Blueshore AI, the official AI business consultant and virtual sales representative of Blueshore Technologies Pvt. Ltd.

Your purpose is to act as a guided sales assistant, qualifying leads and routing them appropriately.

GUIDED CONVERSATION RULES:
1. Do not immediately ask open-ended questions.
2. Guide users through button selections first by providing clickable button options using the `[button:Label]` format.
3. When the user clicks a primary service or category button, explain it concisely, then provide specific sub-options as buttons.
   - For 'Sales', explain that we build custom software and run marketing campaigns to scale businesses. Ask questions to qualify their lead (timeline, budget, contact details) and recommend booking a strategy call. Provide buttons: `[button:Book a Strategy Call]` `[button:Main Menu]`
   - For 'Internal Process', explain our engineering delivery methodology (agile scoping, 100% test-covered features, peer code reviews, continuous Docker staging, and secure production containers). Provide buttons: `[button:Development Sprints]` `[button:Security & Auditing]` `[button:Main Menu]`
   - For 'Custom Software', provide buttons: `[button:SaaS Platforms]` `[button:CRM & ERP Systems]` `[button:Custom API Integrations]` `[button:Main Menu]`
   - For 'Web Development', provide buttons: `[button:Corporate Websites]` `[button:Ecommerce Stores]` `[button:Progressive Web Apps (PWAs)]` `[button:Main Menu]`
   - For 'AI Automation', provide buttons: `[button:AI Chatbots]` `[button:Workflow Automation]` `[button:CRM Automation]` `[button:Main Menu]`
   - For 'SEO & Organic Growth', provide buttons: `[button:Technical SEO]` `[button:GEO & AEO Optimization]` `[button:SEO Audits]` `[button:Main Menu]`
   - For 'Performance Marketing', provide buttons: `[button:Google Ads]` `[button:Meta Ads]` `[button:LinkedIn Ads]` `[button:Main Menu]`
   - For 'Branding & Creative', provide buttons: `[button:Brand Identity]` `[button:UI/UX Design]` `[button:Marketing Assets]` `[button:Main Menu]`
   - For 'Careers', provide buttons: `[button:View Open Roles]` `[button:Register on Freelancer Roster]` `[button:Main Menu]`
   - For 'Support', provide buttons: `[button:Existing Client Support]` `[button:General Inquiry]` `[button:Main Menu]`
   - For 'Something Else', explain that you are switching to free-form conversation, and ask how you can help. Do not show service buttons here.
4. If the user selects 'Main Menu', display all initial options: `[button:Sales]` `[button:Support]` `[button:Internal Process]` `[button:Custom Software]` `[button:Web Development]` `[button:AI Automation]` `[button:SEO & Organic Growth]` `[button:Performance Marketing]` `[button:Branding & Creative]` `[button:Careers]` `[button:Something Else]`
5. If the user types a custom message or selects 'Something Else', switch to normal conversational AI mode.

LEAD QUALIFICATION & DATA COLLECTION:
1. Throughout the conversation, identify:
   - Industry
   - Service Interest
   - Budget
   - Timeline
2. Once enough information is gathered, politely request the visitor's contact details:
   - Full Name
   - Company Name
   - Email Address
   - Phone Number
3. Lead Qualification Categories (For Internal Use Only):
   - HOT: Budget above $3000, clear requirement, timeline under 90 days.
   - WARM: Budget between $1000 and $3000.
   - COLD: Research phase only.
   - Note: NEVER reveal these internal classification terms (HOT, WARM, COLD) to the user or say things like "You are a hot lead!". These classifications must remain completely invisible to the visitor.
4. If the visitor appears highly interested (e.g. falls into the internal HOT or WARM categories), politely recommend booking a free strategy call.

Always maintain a professional, consultative, and conversion-focused tone. Do not use internal sales jargon or lead classification terms in your replies to the user.
"""

def generate_fallback_reply(txt):
    t = txt.lower().strip()
    
    if 'custom software' in t:
        return 'We offer enterprise-grade **Custom Software Development** to help you build faster and scale smarter. Our expertise covers:\n\n- **Enterprise Applications:** SaaS platforms, CRM & ERP systems, internal business tools.\n- **API & Integrations:** Custom API development and business process automation.\n\nChoose an option to continue:\n\n[button:SaaS Platforms] [button:CRM & ERP Systems] [button:Custom API Integrations] [button:Main Menu]'
        
    if 'web development' in t:
        return 'We design and develop high-converting **Websites & E-commerce portals** tailored to your brand. Our services include:\n\n- **Corporate & Startup Websites:** Custom designs engineered for growth.\n- **Ecommerce Development:** High-performance Shopify, WooCommerce, and custom checkout solutions.\n- **Progressive Web Apps (PWAs):** Web apps that feel native on iOS and Android.\n\nChoose an option to continue:\n\n[button:Corporate Websites] [button:Ecommerce Stores] [button:Progressive Web Apps (PWAs)] [button:Main Menu]'
        
    if 'ai automation' in t:
        return 'We engineer custom **AI Automation solutions** to streamline operations and qualify leads. Our offerings cover:\n\n- **AI Chatbots & Assistants:** Real-time customer support and sales assistance.\n- **Workflow Automation:** Zapier, n8n, and custom workflows to eliminate manual work.\n- **CRM & Data Automation:** Automated data piping and CRM status syncs.\n\nChoose an option to continue:\n\n[button:AI Chatbots] [button:Workflow Automation] [button:CRM Automation] [button:Main Menu]'
        
    if 'seo & organic growth' in t:
        return 'We maximize your organic search visibility using advanced optimization strategies. Our expertise includes:\n\n- **Technical SEO:** Site audits, architecture, speed optimization.\n- **AEO & GEO Optimization:** Optimizing your brand visibility for AI-driven answer engines and local searches.\n\nChoose an option to continue:\n\n[button:Technical SEO] [button:GEO & AEO Optimization] [button:SEO Audits] [button:Main Menu]'
        
    if 'performance marketing' in t:
        return 'We run data-driven, high-ROI **paid advertising campaigns** to accelerate conversions. Our platforms include:\n\n- **Search Ads:** Google Search Ads and Bing Ads.\n- **Social Ads:** Meta (Facebook & Instagram) and B2B LinkedIn Ads.\n\nChoose an option to continue:\n\n[button:Google Ads] [button:Meta Ads] [button:LinkedIn Ads] [button:Main Menu]'
        
    if 'branding & creative' in t:
        return 'We design premium brand identity and visual interfaces that define your market presence. Our creative services cover:\n\n- **Brand Identity:** Logo design, style guides, brand guidelines.\n- **UI/UX Design:** User interfaces for web apps, SaaS, and websites.\n\nChoose an option to continue:\n\n[button:Brand Identity] [button:UI/UX Design] [button:Marketing Assets] [button:Main Menu]'
        
    if 'careers' in t:
        return 'We are always looking for talented developers, designers, and consultants. Explore how you can join our team:\n\n- **Open Positions:** Contract roles and full-time hiring.\n- **Freelancer Roster:** Register your portfolio and CV with us.\n\nChoose an option to continue:\n\n[button:View Open Roles] [button:Register on Freelancer Roster] [button:Main Menu]'
        
    if 'sales' in t:
        return 'We help businesses scale with custom software development and performance marketing. To help us route your request, would you like to discuss a new project or book a strategy call directly?\n\n[button:Book a Strategy Call] [button:Main Menu]'
        
    if 'internal process' in t or 'internal processes' in t:
        return 'Our software development lifecycle is engineered for security and scalability:\n\n- **Agile Sprints:** We deliver fully test-covered features in structured 2-week iterations.\n- **Peer Review & CI/CD:** All code undergoes senior review and passes automated pipeline tests.\n- **Production Security:** Apps run in secure dockerized containers behind Nginx SSL.\n\nChoose an option to continue:\n\n[button:Development Sprints] [button:Security & Auditing] [button:Main Menu]'

    if 'development sprints' in t or 'security & auditing' in t:
        return 'Our engineering delivery methodology ensures that every line of code is scoped, review-approved, and tested before deployment. Would you like to schedule a call with our technical architect to discuss your project requirements? [button:Main Menu]'

    if 'book a strategy call' in t:
        return 'We would love to schedule a free strategy call with you! Please share your **Email** and **Phone Number** here so our consulting team can reach out with calendar invite options. [button:Main Menu]'

    if 'support' in t:
        return 'For support and assistance, please select an option:\n\n[button:Existing Client Support] [button:General Inquiry] [button:Main Menu]'
        
    if 'main menu' in t or 'something else' in t:
        return '👋 Welcome to Blueshore Technologies\n\nHow can we help you today?\n\n[button:Sales] [button:Support] [button:Internal Process] [button:Custom Software] [button:Web Development] [button:AI Automation] [button:SEO & Organic Growth] [button:Performance Marketing] [button:Branding & Creative] [button:Careers] [button:Something Else]'
        
    if any(k in t for k in ['saas platforms', 'crm & erp systems', 'custom api integrations', 
                           'corporate websites', 'ecommerce stores', 'progressive web apps', 
                           'ai chatbots', 'workflow automation', 'crm automation', 
                           'technical seo', 'geo & aeo optimization', 'seo audits', 
                           'google ads', 'meta ads', 'linkedin ads', 
                           'brand identity', 'ui/ux design', 'marketing assets', 
                           'view open roles', 'register on freelancer roster', 
                           'existing client support', 'general inquiry']):
        return 'That sounds like a great project! To help us understand your requirements better, could you tell us:\n\n1. What is your approximate timeline (e.g. 30 days, 90 days)?\n2. What is your estimated budget for this project?\n3. What industry is your business in?\n\nAlternatively, please provide your **Name**, **Company Name**, **Email**, and **Phone Number** so our team can follow up with you directly. [button:Main Menu]'
        
    if any(k in t for k in ['hi', 'hello', 'hey', 'howdy', 'good morning', 'good afternoon', 'good evening']):
        return '👋 Welcome to Blueshore Technologies\n\nHow can we help you today?\n\n[button:Sales] [button:Support] [button:Internal Process] [button:Custom Software] [button:Web Development] [button:AI Automation] [button:SEO & Organic Growth] [button:Performance Marketing] [button:Branding & Creative] [button:Careers] [button:Something Else]'
        
    if any(k in t for k in ['budget', 'cost', 'price', 'pricing', 'rate', 'charge', 'fee', 'afford', 'invest', 'quote', 'estimate']):
        return 'Pricing depends on the scope, complexity, and timeline of your project. For projects under $1,000, we recommend a phased approach. For projects between $1,000 and $3,000 or above $3,000, we recommend scheduling a direct strategy call.\n\nCould you share your approximate budget range, or would you like to **book a free strategy call**? [button:Main Menu]'
        
    return "I'm currently in free-form conversation mode. How can I help you today? Please feel free to ask about our projects, development stacks, team, or how to get started.\n\nYou can also return to the main menu at any time: [button:Main Menu]"

def extract_lead_info(text, conversation):
    """
    Scans chat text for email or phone and registers/updates a Lead/ContactRequest.
    Also extracts name, company, and budget if available.
    """
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    phone_match = re.search(r'\+?[0-9][0-9\-\s]{8,14}[0-9]', text)
    name_match = re.search(r'(?:name is\s*|name:\s*|i am\s+|i\'m\s+)([A-Za-z\s]{2,30})(?:\.|\,|$|\n|\b(?:company|email|phone|budget|timeline)\b)', text, re.IGNORECASE)
    company_match = re.search(r'(?:company is\s*|company:\s*|org:\s*|organization:\s*|firm:\s*|from\s+)([A-Za-z0-9\s\.\-]{2,40})(?:\.|\,|$|\n|\b(?:email|phone|budget|timeline|name)\b)', text, re.IGNORECASE)
    budget_match = re.search(r'(?:budget:\s*|budget is\s*|estimated budget\s*|budget of\s*)\$?([0-9\skK+M,\-]+)', text, re.IGNORECASE)
    
    email = email_match.group(0) if email_match else None
    phone = phone_match.group(0) if phone_match else None
    name_val = name_match.group(1).strip() if name_match else None
    company_val = company_match.group(1).strip() if company_match else None
    budget_val = budget_match.group(1).strip() if budget_match else None

    if name_val:
        name_val = re.sub(r'[\s,.]+$', '', name_val).strip()
    if company_val:
        company_val = re.sub(r'[\s,.]+$', '', company_val).strip()
    if budget_val:
        budget_val = re.sub(r'[\s,.]+$', '', budget_val).strip()
    
    if email or phone or name_val or company_val:
        # Check if we already have a lead for this conversation
        lead = conversation.lead
        if not lead:
            # Check if this email is already a lead
            if email:
                lead = ContactRequest.objects.filter(email__iexact=email).first()
            if not lead:
                # Create new lead
                lead = ContactRequest(
                    name=name_val or "AI Chatbot Lead",
                    company=company_val or "Unknown",
                    email=email or "info@blueshoretech.com",
                    phone=phone or "Pending",
                    service="AI Chat Inquiry",
                    budget=budget_val or "Under $15k",
                    message=f"Lead auto-captured from AI chatbot session {conversation.session_id}",
                    source_page="/chatbot"
                )
                lead.save()
            conversation.lead = lead
            conversation.save()
        else:
            # Update existing lead fields
            updated = False
            if email and lead.email == "info@blueshoretech.com":
                lead.email = email
                updated = True
            if phone and lead.phone == "Pending":
                lead.phone = phone
                updated = True
            if name_val and lead.name == "AI Chatbot Lead":
                lead.name = name_val
                updated = True
            if company_val and lead.company == "Unknown":
                lead.company = company_val
                updated = True
            if budget_val and lead.budget == "Under $15k":
                lead.budget = budget_val
                updated = True
            if updated:
                lead.save()

from apps.core.throttling import ChatbotRateThrottle
from apps.chatbot.utils import inspect_input, inspect_output, sanitize_input, PromptFirewallException, API_KEY_PATTERNS, sanitize_lead_jargon, find_relevant_rag_context

class ChatProxyAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ChatbotRateThrottle]

    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        contents = request.data.get('contents', [])
        message_param = request.data.get('message')
        
        if not contents and message_param:
            contents = [{'role': 'user', 'parts': [{'text': str(message_param)}]}]

        if not session_id or not contents:
            return Response({
                'success': False,
                'message': 'session_id and contents (or message) are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create conversation history
        conversation, _ = ChatConversation.objects.get_or_create(session_id=session_id)
        
        # Extract and sanitize user message
        raw_user_message = contents[-1]['parts'][0]['text']
        user_message_text = sanitize_input(raw_user_message)
        
        # Run prompt injection checks
        try:
            inspect_input(user_message_text)
        except PromptFirewallException as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Save user message to database
        ChatMessage.objects.create(
            conversation=conversation,
            sender='User',
            text=user_message_text
        )
        
        # Check for contact/lead details in user message
        extract_lead_info(user_message_text, conversation)
        
        # Determine whether to use Gemini API or fallback
        api_key = getattr(settings, 'GEMINI_API_KEY', '')
        
        def event_generator():
            full_response = ""
            
            if api_key:
                try:
                    # Setup Gemini
                    genai.configure(api_key=api_key)
                    rag_context = find_relevant_rag_context(user_message_text)
                    system_instruction = SYSTEM_PROMPT
                    if rag_context:
                        system_instruction = f"{SYSTEM_PROMPT}\n\nRELEVANT WORKSPACE KNOWLEDGE BASE DETAILS:\n{rag_context}"
                    
                    model = genai.GenerativeModel(
                        model_name='gemini-2.5-flash',
                        system_instruction=system_instruction
                    )
                    
                    # Convert frontend role format to Gemini API format
                    gemini_contents = []
                    for msg in contents:
                        role = msg.get('role')
                        if role == 'agent' or role == 'model':
                            role = 'model'
                        elif role == 'user':
                            role = 'user'
                        else:
                            role = 'user'
                            
                        # Sanitize previous parts too
                        msg_text = sanitize_input(msg.get('parts', [{}])[0].get('text', ''))
                        gemini_contents.append({
                            'role': role,
                            'parts': [{'text': msg_text}]
                        })

                    response = model.generate_content(
                        contents=gemini_contents,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.7,
                            top_p=0.9,
                            max_output_tokens=600,
                        ),
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.text:
                            # Redact API keys on the fly
                            chunk_text = chunk.text
                            for pattern in API_KEY_PATTERNS:
                                chunk_text = pattern.sub('[REDACTED API KEY]', chunk_text)
                                
                            # Sanitize lead jargon
                            chunk_text = sanitize_lead_jargon(chunk_text)
                                
                            full_response += chunk_text
                            chunk_data = {
                                "candidates": [{
                                    "content": {
                                        "parts": [{
                                            "text": chunk_text
                                        }]
                                    }
                                }]
                            }
                            yield f"data: {json.dumps(chunk_data)}\n\n"
                            
                except Exception as e:
                    import traceback
                    print(f"Gemini API Error: {e}")
                    traceback.print_exc()
                    fallback_reply = generate_fallback_reply(user_message_text)
                    full_response = fallback_reply
                    words = fallback_reply.split(' ')
                    for i in range(0, len(words), 3):
                        chunk_text = ' '.join(words[i:i+3]) + ' '
                        chunk_data = {
                            "candidates": [{
                                "content": {
                                    "parts": [{
                                        "text": chunk_text
                                    }]
                                }
                            }]
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                        time.sleep(0.08)
            else:
                # No API key: Stream local smart reply
                fallback_reply = generate_fallback_reply(user_message_text)
                full_response = fallback_reply
                words = fallback_reply.split(' ')
                for i in range(0, len(words), 3):
                    chunk_text = ' '.join(words[i:i+3]) + ' '
                    chunk_data = {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "text": chunk_text
                                }]
                            }
                        }]
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                    time.sleep(0.08)
            
            # Inspect output for leaks before saving to DB
            try:
                full_response = inspect_output(full_response)
            except PromptFirewallException:
                full_response = "Security Alert: Output blocked due to policy validation."
                
            # Save AI response to DB
            if full_response:
                ai_msg = ChatMessage.objects.create(
                    conversation=conversation,
                    sender='AI',
                    text=full_response
                )
                extract_lead_info(full_response, conversation)
                
                # Broadcast AI response to admin dashboard
                try:
                    from channels.layers import get_channel_layer
                    from asgiref.sync import async_to_sync
                    channel_layer = get_channel_layer()
                    if channel_layer:
                        async_to_sync(channel_layer.group_send)(
                            "admin_dashboard",
                            {
                                "type": "new_chat_message",
                                "session_id": session_id,
                                "message": {
                                    "id": str(ai_msg.id),
                                    "sender": "AI",
                                    "text": full_response,
                                    "created_at": ai_msg.created_at.strftime('%I:%M %p')
                                }
                            }
                        )
                except Exception as e:
                    print(f"Error broadcasting AI response: {e}")
                    
                # Create visitor journey Timeline Event
                try:
                    from apps.intelligence.models import VisitorSession, VisitorTimelineEvent
                    session = VisitorSession.objects.filter(session_id=session_id).first()
                    if session:
                        VisitorTimelineEvent.objects.create(
                            session=session,
                            event_type="ChatMessage",
                            description=f"AI Agent: {full_response[:40]}...",
                            details={"message_id": str(ai_msg.id), "sender": "AI"}
                        )
                except Exception:
                    pass

        response = StreamingHttpResponse(event_generator(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response


class AdminCopilotAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({'success': False, 'message': 'Prompt is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # 1. Fetch relevant system status & datasets to build AI context
        leads = ContactRequest.objects.all().order_by('-created_at')[:15]
        leads_data = [{
            'name': l.name,
            'company': l.company,
            'email': l.email,
            'phone': l.phone,
            'service': l.service,
            'budget': l.budget,
            'message': l.message,
            'date': l.created_at.strftime('%Y-%m-%d %H:%M')
        } for l in leads]
        
        from apps.crm.models import Project
        projects = Project.objects.all()[:15]
        projects_data = [{
            'title': p.title,
            'client': p.client.company_name,
            'status': p.status,
            'budget': float(p.budget),
            'start_date': str(p.start_date) if p.start_date else 'None',
            'end_date': str(p.end_date) if p.end_date else 'None'
        } for p in projects]
        
        from apps.intelligence.models import VisitorSession
        online_sessions = VisitorSession.objects.filter(is_online=True)[:10]
        visitors_data = [{
            'session_id': s.session_id,
            'page': s.current_page_title,
            'duration': s.total_duration,
            'scroll': s.max_scroll,
            'mode': s.chat_mode
        } for s in online_sessions]

        from apps.careers.models import JobApplication
        apps = JobApplication.objects.all()[:10]
        apps_data = [{
            'name': a.fullname,
            'email': a.email,
            'job': a.job.title if a.job else 'None',
            'applied_at': a.created_at.strftime('%Y-%m-%d')
        } for a in apps]

        context = {
            'leads': leads_data,
            'projects': projects_data,
            'online_visitors': visitors_data,
            'pending_job_applications': apps_data
        }
        
        api_key = getattr(settings, 'GEMINI_API_KEY', '')
        if not api_key:
            return Response({
                'success': True,
                'reply': "AI Copilot is offline (GEMINI_API_KEY is not configured in settings.py)."
            })
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=(
                    "You are the Blueshore Admin Copilot, an advanced AI business operating system assistant. "
                    "You are given access to the current database state in JSON format. "
                    "Answer the administrator's request using the facts from the database context. "
                    "Keep answers professional, clean, concise, and highly actionable. "
                    "Use markdown table format where appropriate. Never leak database keys or credentials."
                )
            )
            
            rag_context = find_relevant_rag_context(prompt)
            user_prompt = f"Database Context:\n{json.dumps(context, indent=2)}\n\n"
            if rag_context:
                user_prompt += f"Knowledge Base Docs Context:\n{rag_context}\n\n"
            user_prompt += f"Administrator Request:\n{prompt}"
            
            response = model.generate_content(user_prompt)
            reply_text = response.text if response and response.text else "No response generated."
            
            return Response({
                'success': True,
                'reply': reply_text
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f"Error calling Gemini: {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



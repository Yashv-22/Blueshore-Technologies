/* ── Blueshore AI Agent — Real-Time Chat Engine ── */
(function () {
    'use strict';

    /* ——————— State ——————— */
    var GEMINI_KEY = localStorage.getItem('blueshore-gemini-key') || '';
    var conversationHistory = [];
    var isStreaming = false;
    var session_id = localStorage.getItem('blueshore-chat-session-id') || '';
    if (!session_id) {
        session_id = 'session_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        localStorage.setItem('blueshore-chat-session-id', session_id);
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var SYSTEM_PROMPT = [
        "You are Blueshore AI, the official AI business consultant and virtual sales representative of Blueshore Technologies Pvt. Ltd.",
        "",
        "Your purpose is to act as a guided sales assistant, qualifying leads and routing them appropriately.",
        "",
        "GUIDED CONVERSATION RULES:",
        "1. Do not immediately ask open-ended questions.",
        "2. Guide users through button selections first by providing clickable button options using the `[button:Label]` format.",
        "3. When the user clicks a primary service button, explain that service concisely, then provide specific sub-options as buttons.",
        "   - For 'Custom Software', provide buttons: `[button:SaaS Platforms]` `[button:CRM & ERP Systems]` `[button:Custom API Integrations]` `[button:Main Menu]`",
        "   - For 'Web Development', provide buttons: `[button:Corporate Websites]` `[button:Ecommerce Stores]` `[button:Progressive Web Apps (PWAs)]` `[button:Main Menu]`",
        "   - For 'AI Automation', provide buttons: `[button:AI Chatbots]` `[button:Workflow Automation]` `[button:CRM Automation]` `[button:Main Menu]`",
        "   - For 'SEO & Organic Growth', provide buttons: `[button:Technical SEO]` `[button:GEO & AEO Optimization]` `[button:SEO Audits]` `[button:Main Menu]`",
        "   - For 'Performance Marketing', provide buttons: `[button:Google Ads]` `[button:Meta Ads]` `[button:LinkedIn Ads]` `[button:Main Menu]`",
        "   - For 'Branding & Creative', provide buttons: `[button:Brand Identity]` `[button:UI/UX Design]` `[button:Marketing Assets]` `[button:Main Menu]`",
        "   - For 'Careers', provide buttons: `[button:View Open Roles]` `[button:Register on Freelancer Roster]` `[button:Main Menu]`",
        "   - For 'Support', provide buttons: `[button:Existing Client Support]` `[button:General Inquiry]` `[button:Main Menu]`",
        "   - For 'Something Else', explain that you are switching to free-form conversation, and ask how you can help. Do not show service buttons here.",
        "4. If the user selects 'Main Menu', display all initial options: `[button:Sales]` `[button:Support]` `[button:Internal Process]` `[button:Custom Software]` `[button:Web Development]` `[button:AI Automation]` `[button:SEO & Organic Growth]` `[button:Performance Marketing]` `[button:Branding & Creative]` `[button:Careers]` `[button:Something Else]`",
        "5. If the user types a custom message or selects 'Something Else', switch to normal conversational AI mode.",
        "",
        "LEAD QUALIFICATION & DATA COLLECTION:",
        "1. Throughout the conversation, identify:",
        "   - Industry",
        "   - Service Interest",
        "   - Budget",
        "   - Timeline",
        "2. Once enough information is gathered, politely request the visitor's contact details:",
        "   - Full Name",
        "   - Company Name",
        "   - Email Address",
        "   - Phone Number",
        "3. Lead Qualification Categories:",
        "   - HOT: Budget above $3000, clear requirement, timeline under 90 days.",
        "   - WARM: Budget between $1000 and $3000.",
        "   - COLD: Research phase only.",
        "4. If the visitor appears highly interested (HOT or WARM lead), recommend booking a free strategy call.",
        "",
        "Always maintain a professional, consultative, and conversion-focused tone."
    ].join('\n');

    /* ——————— Utility: simple Markdown → HTML ——————— */
    function renderMarkdown(text) {
        // Parse button tags [button:Label]
        var buttonRegex = /\[button:(.+?)\]/g;
        if (buttonRegex.test(text)) {
            text = text.replace(buttonRegex, function(match, label) {
                return '<button class="ai-chat-quick-btn" onclick="sendQuickAction(\'' + label.replace(/'/g, "\\'") + '\')">' + label + '</button>';
            });
        }
        return text
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/`(.+?)`/g, '<code style="background:rgba(55,144,255,0.12);padding:1px 5px;border-radius:4px;font-size:12px;">$1</code>')
            .replace(/^[\s]*[-•]\s+(.+)/gm, '<li style="margin-left:16px;list-style:disc;">$1</li>')
            .replace(/(<li[^>]*>.*<\/li>\n?)+/g, function(m){ return '<ul style="margin:6px 0;">'+m+'</ul>'; })
            .replace(/\n/g, '<br>');
    }

    /* ——————— Toggle Widget ——————— */
    window.toggleAIAgent = function () {
        var widget = document.getElementById('ai-agent-widget');
        if (!widget) return;
        widget.classList.toggle('active');
        
        var waBtn = document.querySelector('a[href*="wa.me"]');
        var toggleBtn = document.getElementById('ai-agent-toggle-btn');
        var isActive = widget.classList.contains('active');

        if (waBtn) {
            waBtn.style.opacity = isActive ? '0' : '1';
            waBtn.style.pointerEvents = isActive ? 'none' : 'auto';
        }
        if (toggleBtn) {
            toggleBtn.style.opacity = isActive ? '0' : '1';
            toggleBtn.style.pointerEvents = isActive ? 'none' : 'auto';
        }

        if (isActive) {
            var msgs = document.getElementById('ai-chat-messages');
            if (msgs) msgs.scrollTop = msgs.scrollHeight;
            setTimeout(function () {
                var inp = document.getElementById('ai-chat-input-el');
                if (inp) inp.focus();
            }, 200);
        }
    };

    window.toggleWelcomeDropdown = function() {
        var trigger = document.getElementById('ai-chat-welcome-trigger');
        var content = document.getElementById('ai-chat-welcome-content');
        if (!trigger || !content) return;
        
        trigger.classList.toggle('active');
        content.classList.toggle('show');
        
        var arrow = trigger.querySelector('.dropdown-arrow');
        if (arrow) {
            arrow.textContent = trigger.classList.contains('active') ? '▲' : '▼';
        }
        
        var msgs = document.getElementById('ai-chat-messages');
        if (msgs) {
            setTimeout(function() {
                msgs.scrollTop = msgs.scrollHeight;
            }, 50);
        }
    };

    /* ——————— API Key Config ——————— */
    window.openApiKeySetup = function () {
        var panel = document.getElementById('api-key-panel');
        if (panel) panel.classList.toggle('hidden');
    };

    window.saveApiKey = function () {
        var inp = document.getElementById('gemini-key-input');
        var key = inp ? inp.value.trim() : '';
        if (key) {
            GEMINI_KEY = key;
            localStorage.setItem('blueshore-gemini-key', key);
            var panel = document.getElementById('api-key-panel');
            if (panel) panel.classList.add('hidden');
            var badge = document.getElementById('ai-mode-badge');
            if (badge) {
                badge.textContent = '⚡ AI Powered';
                badge.className = 'ai-mode-badge ai-connected';
            }
            /* Inject a confirmation agent message */
            appendAgentMessage('⚡ AI engine connected! I\'m now powered by real-time intelligence. Ask me anything about Blueshore Technologies — projects, stacks, pricing, timelines.');
        }
    };

    window.clearApiKey = function () {
        GEMINI_KEY = '';
        localStorage.removeItem('blueshore-gemini-key');
        var badge = document.getElementById('ai-mode-badge');
        if (badge) {
            badge.textContent = 'Smart Replies';
            badge.className = 'ai-mode-badge';
        }
        var panel = document.getElementById('api-key-panel');
        if (panel) panel.classList.add('hidden');
        appendAgentMessage('API key removed. I\'m now using smart preset replies. You can reconnect anytime via the ⚙ settings icon.');
    };

    /* ——————— Helpers ——————— */
    function getMessagesContainer() {
        return document.getElementById('ai-chat-messages');
    }

    function scrollToBottom() {
        var mc = getMessagesContainer();
        if (mc) mc.scrollTop = mc.scrollHeight;
    }

    function appendAgentMessage(html, sender) {
        var mc = getMessagesContainer();
        var msg = document.createElement('div');
        if (sender === 'Admin') {
            msg.className = 'ai-chat-msg agent admin';
        } else {
            msg.className = 'ai-chat-msg agent';
        }
        msg.innerHTML = renderMarkdown(html);
        mc.appendChild(msg);
        scrollToBottom();
    }

    function showTyping() {
        var mc = getMessagesContainer();
        var el = document.createElement('div');
        el.className = 'typing-indicator';
        el.id = 'ai-typing-indicator';
        el.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        mc.appendChild(el);
        scrollToBottom();
    }

    function removeTyping() {
        var el = document.getElementById('ai-typing-indicator');
        if (el) el.remove();
    }

    function setInputEnabled(enabled) {
        var inp = document.getElementById('ai-chat-input-el');
        var btn = document.getElementById('ai-send-btn');
        if (inp) { inp.disabled = !enabled; if (enabled) inp.focus(); }
        if (btn) btn.disabled = !enabled;
    }

    /* ——————— Fallback: Smart Pattern Matching ——————— */
    function generateFallbackReply(txt) {
        var t = txt.toLowerCase().trim();
        
        if (t.indexOf('custom software') !== -1) {
            return 'We offer enterprise-grade **Custom Software Development** to help you build faster and scale smarter. Our expertise covers:\n\n- **Enterprise Applications:** SaaS platforms, CRM & ERP systems, internal business tools.\n- **API & Integrations:** Custom API development and business process automation.\n\nChoose an option to continue:\n\n[button:SaaS Platforms] [button:CRM & ERP Systems] [button:Custom API Integrations] [button:Main Menu]';
        }
        if (t.indexOf('web development') !== -1) {
            return 'We design and develop high-converting **Websites & E-commerce portals** tailored to your brand. Our services include:\n\n- **Corporate & Startup Websites:** Custom designs engineered for growth.\n- **Ecommerce Development:** High-performance Shopify, WooCommerce, and custom checkout solutions.\n- **Progressive Web Apps (PWAs):** Web apps that feel native on iOS and Android.\n\nChoose an option to continue:\n\n[button:Corporate Websites] [button:Ecommerce Stores] [button:Progressive Web Apps (PWAs)] [button:Main Menu]';
        }
        if (t.indexOf('ai automation') !== -1) {
            return 'We engineer custom **AI Automation solutions** to streamline operations and qualify leads. Our offerings cover:\n\n- **AI Chatbots & Assistants:** Real-time customer support and sales assistance.\n- **Workflow Automation:** Zapier, n8n, and custom workflows to eliminate manual work.\n- **CRM & Data Automation:** Automated data piping and CRM status syncs.\n\nChoose an option to continue:\n\n[button:AI Chatbots] [button:Workflow Automation] [button:CRM Automation] [button:Main Menu]';
        }
        if (t.indexOf('seo & organic growth') !== -1) {
            return 'We maximize your organic search visibility using advanced optimization strategies. Our expertise includes:\n\n- **Technical SEO:** Site audits, architecture, speed optimization.\n- **AEO & GEO Optimization:** Optimizing your brand visibility for AI-driven answer engines and local searches.\n\nChoose an option to continue:\n\n[button:Technical SEO] [button:GEO & AEO Optimization] [button:SEO Audits] [button:Main Menu]';
        }
        if (t.indexOf('performance marketing') !== -1) {
            return 'We run data-driven, high-ROI **paid advertising campaigns** to accelerate conversions. Our platforms include:\n\n- **Search Ads:** Google Search Ads and Bing Ads.\n- **Social Ads:** Meta (Facebook & Instagram) and B2B LinkedIn Ads.\n\nChoose an option to continue:\n\n[button:Google Ads] [button:Meta Ads] [button:LinkedIn Ads] [button:Main Menu]';
        }
        if (t.indexOf('branding & creative') !== -1) {
            return 'We design premium brand identity and visual interfaces that define your market presence. Our creative services cover:\n\n- **Brand Identity:** Logo design, style guides, brand guidelines.\n- **UI/UX Design:** User interfaces for web apps, SaaS, and websites.\n\nChoose an option to continue:\n\n[button:Brand Identity] [button:UI/UX Design] [button:Marketing Assets] [button:Main Menu]';
        }
        if (t.indexOf('careers') !== -1) {
            return 'We are always looking for talented developers, designers, and consultants. Explore how you can join our team:\n\n- **Open Positions:** Contract roles and full-time hiring.\n- **Freelancer Roster:** Register your portfolio and CV with us.\n\nChoose an option to continue:\n\n[button:View Open Roles] [button:Register on Freelancer Roster] [button:Main Menu]';
        }
        if (t.indexOf('sales') !== -1) {
            return 'We help businesses scale with custom software development and performance marketing. To help us route your request, would you like to discuss a new project or book a strategy call directly?\n\n[button:Book a Strategy Call] [button:Main Menu]';
        }
        if (t.indexOf('internal process') !== -1 || t.indexOf('internal processes') !== -1) {
            return 'Our software development lifecycle is engineered for security and scalability:\n\n- **Agile Sprints:** We deliver fully test-covered features in structured 2-week iterations.\n- **Peer Review & CI/CD:** All code undergoes senior review and passes automated pipeline tests.\n- **Production Security:** Apps run in secure dockerized containers behind Nginx SSL.\n\nChoose an option to continue:\n\n[button:Development Sprints] [button:Security & Auditing] [button:Main Menu]';
        }
        if (t.indexOf('development sprints') !== -1 || t.indexOf('security & auditing') !== -1) {
            return 'Our engineering delivery methodology ensures that every line of code is scoped, review-approved, and tested before deployment. Would you like to schedule a call with our technical architect to discuss your project requirements? [button:Main Menu]';
        }
        if (t.indexOf('book a strategy call') !== -1) {
            return 'We would love to schedule a free strategy call with you! Please share your **Email** and **Phone Number** here so our consulting team can reach out with calendar invite options. [button:Main Menu]';
        }
        if (t.indexOf('support') !== -1) {
            return 'For support and assistance, please select an option:\n\n[button:Existing Client Support] [button:General Inquiry] [button:Main Menu]';
        }
        if (t.indexOf('main menu') !== -1 || t.indexOf('something else') !== -1) {
            return '👋 Welcome to Blueshore Technologies\n\nHow can we help you today?\n\n[button:Sales] [button:Support] [button:Internal Process] [button:Custom Software] [button:Web Development] [button:AI Automation] [button:SEO & Organic Growth] [button:Performance Marketing] [button:Branding & Creative] [button:Careers] [button:Something Else]';
        }
        if (t.indexOf('saas platforms') !== -1 || t.indexOf('crm & erp systems') !== -1 || t.indexOf('custom api integrations') !== -1 ||
            t.indexOf('corporate websites') !== -1 || t.indexOf('ecommerce stores') !== -1 || t.indexOf('progressive web apps') !== -1 ||
            t.indexOf('ai chatbots') !== -1 || t.indexOf('workflow automation') !== -1 || t.indexOf('crm automation') !== -1 ||
            t.indexOf('technical seo') !== -1 || t.indexOf('geo & aeo optimization') !== -1 || t.indexOf('seo audits') !== -1 ||
            t.indexOf('google ads') !== -1 || t.indexOf('meta ads') !== -1 || t.indexOf('linkedin ads') !== -1 ||
            t.indexOf('brand identity') !== -1 || t.indexOf('ui/ux design') !== -1 || t.indexOf('marketing assets') !== -1 ||
            t.indexOf('view open roles') !== -1 || t.indexOf('register on freelancer roster') !== -1 ||
            t.indexOf('existing client support') !== -1 || t.indexOf('general inquiry') !== -1) {
            return 'That sounds like a great project! To help us understand your requirements better, could you tell us:\n\n1. What is your approximate timeline (e.g. 30 days, 90 days)?\n2. What is your estimated budget for this project?\n3. What industry is your business in?\n\nAlternatively, please provide your **Name**, **Company Name**, **Email**, and **Phone Number** so our team can follow up with you directly. [button:Main Menu]';
        }
        if (/^(hi|hello|hey|howdy|good\s*(morning|afternoon|evening))/.test(t)) {
            return '👋 Welcome to Blueshore Technologies\n\nHow can we help you today?\n\n[button:Sales] [button:Support] [button:Internal Process] [button:Custom Software] [button:Web Development] [button:AI Automation] [button:SEO & Organic Growth] [button:Performance Marketing] [button:Branding & Creative] [button:Careers] [button:Something Else]';
        }
        if (/budget|cost|price|pricing|rate|charge|fee|afford|invest|quote|estimate/.test(t)) {
            return 'Pricing depends on the scope, complexity, and timeline of your project. For projects under $1,000, we recommend a phased approach. For projects between $1,000 and $3,000 (WARM) or above $3,000 (HOT), we recommend scheduling a direct strategy call.\n\nCould you share your approximate budget range, or would you like to **book a free strategy call**? [button:Main Menu]';
        }
        
        return 'I\'m currently in free-form conversation mode. How can I help you today? Please feel free to ask about our projects, development stacks, team, or how to get started.\n\nYou can also return to the main menu at any time: [button:Main Menu]';
    }

    /* ——————— Gemini API: Streaming Fetch ——————— */
    async function callGeminiStreaming(userText, agentMsgEl) {
        conversationHistory.push({ role: 'user', parts: [{ text: userText }] });

        var url = '/api/chatbot/chat/';
        var csrfToken = getCookie('csrftoken') || '';

        var body = {
            session_id: session_id,
            contents: conversationHistory
        };

        var response = await fetch(url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            var errText = await response.text();
            throw new Error('Server ' + response.status + ': ' + errText.substring(0, 200));
        }

        var reader = response.body.getReader();
        var decoder = new TextDecoder();
        var fullText = '';
        var buffer = '';

        while (true) {
            var result = await reader.read();
            if (result.done) break;

            buffer += decoder.decode(result.value, { stream: true });
            var lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (var i = 0; i < lines.length; i++) {
                var line = lines[i].trim();
                if (!line.startsWith('data: ')) continue;
                var jsonStr = line.slice(6);
                if (jsonStr === '[DONE]') continue;

                try {
                    var data = JSON.parse(jsonStr);
                    if (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts) {
                        var parts = data.candidates[0].content.parts;
                        for (var p = 0; p < parts.length; p++) {
                            if (parts[p].text) {
                                fullText += parts[p].text;
                                agentMsgEl.innerHTML = renderMarkdown(fullText) + '<span class="streaming-cursor"></span>';
                                scrollToBottom();
                            }
                        }
                    }
                } catch (e) { /* skip malformed chunks */ }
            }
        }

        /* Final render without cursor */
        agentMsgEl.innerHTML = renderMarkdown(fullText);
        conversationHistory.push({ role: 'model', parts: [{ text: fullText }] });

        if (conversationHistory.length > 40) {
            conversationHistory = conversationHistory.slice(-40);
        }

        return fullText;
    }

    /* ——————— Send Message (Main Entry) ——————— */
    window.sendChatMessage = async function () {
        if (isStreaming) return;

        var input = document.getElementById('ai-chat-input-el');
        var txt = input.value.trim();
        if (!txt) return;
        input.value = '';

        var mc = getMessagesContainer();

        /* Append user message */
        var userMsg = document.createElement('div');
        userMsg.className = 'ai-chat-msg user';
        userMsg.textContent = txt;
        mc.appendChild(userMsg);
        scrollToBottom();

        // Send to WebSocket so telemetry/live-view knows
        if (telemetrySocket && telemetrySocket.readyState === WebSocket.OPEN) {
            telemetrySocket.send(JSON.stringify({
                type: 'chat_message',
                text: txt
            }));
        }

        // If mode is Human, we stop here and wait for admin's reply via WS!
        if (currentChatMode === 'Human') {
            return;
        }

        isStreaming = true;
        setInputEnabled(false);

        /* ── Real-time AI Mode via Django Server Proxy ── */
        showTyping();

        var agentMsg = document.createElement('div');
        agentMsg.className = 'ai-chat-msg agent';
        agentMsg.innerHTML = '';

        try {
            removeTyping();
            mc.appendChild(agentMsg);
            scrollToBottom();

            await callGeminiStreaming(txt, agentMsg);
        } catch (err) {
            removeTyping();
            if (!agentMsg.parentNode) mc.appendChild(agentMsg);
            agentMsg.innerHTML = '⚠️ <strong>Connection issue:</strong> ' + err.message.substring(0, 120) + '<br><br>Falling back to smart replies...';
            setTimeout(function () {
                appendAgentMessage(generateFallbackReply(txt), 'AI');
            }, 600);
        }

        isStreaming = false;
        setInputEnabled(true);
    };

    window.sendQuickAction = function (label) {
        if (isStreaming) return;
        var input = document.getElementById('ai-chat-input-el');
        if (input) {
            input.value = label;
        }
        window.sendChatMessage();
    };

    /* ——————— DOM Injections ── */
    function injectChatbot() {
        if (document.getElementById('ai-agent-widget')) return;

        // 1. Create Widget HTML Structure
        var widgetHtml = 
            '<!-- Header -->' +
            '<div class="ai-chat-header text-left">' +
            '    <div class="flex items-center gap-3">' +
            '        <div class="ai-chat-avatar">' +
            '            <svg style="width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; display: inline-block; vertical-align: middle;" viewBox="0 0 24 24">' +
            '                <rect x="3" y="11" width="18" height="10" rx="2"></rect>' +
            '                <circle cx="8.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '                <circle cx="15.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '                <path d="M10 19h4"></path>' +
            '                <path d="M12 6V11M12 3a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3z"></path>' +
            '                <path d="M3 14H1.5M21 14h1.5"></path>' +
            '            </svg>' +
            '        </div>' +
            '        <div>' +
            '            <h4 class="text-sm font-semibold text-slate-900 dark:text-white leading-tight">Blueshore AI</h4>' +
            '            <div class="flex items-center gap-1.5 mt-0.5">' +
            '                <span class="w-1.5 h-1.5 rounded-full bg-[#22c55e] animate-pulse"></span>' +
            '                <span id="ai-mode-badge" class="ai-mode-badge ai-connected">⚡ AI Powered</span>' +
            '            </div>' +
            '        </div>' +
            '    </div>' +
            '    <div class="flex items-center gap-1">' +
            '        <button onclick="toggleAIAgent()" class="text-slate-500 hover:text-[#3790ff] transition-colors shrink-0 p-1">' +
            '            <span class="material-symbols-outlined text-lg">close</span>' +
            '        </button>' +
            '    </div>' +
            '</div>' +
            '<div id="ai-chat-messages" class="ai-chat-messages text-left">' +
            '    <div class="ai-chat-msg agent">' +
            '        👋 Welcome to **Blueshore Technologies**! Your trusted technology consulting and digital growth partner.<br><br>How can we help you scale your business today?<br>' +
            '        <button id="ai-chat-welcome-trigger" class="ai-chat-dropdown-btn" onclick="toggleWelcomeDropdown()">Explore Options <span class="dropdown-arrow">▼</span></button>' +
            '        <div id="ai-chat-welcome-content" class="ai-chat-dropdown-content">' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Sales\')">Sales</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Support\')">Support</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Internal Process\')">Internal Process</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Custom Software\')">Custom Software</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Web Development\')">Web Development</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'AI Automation\')">AI Automation</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'SEO & Organic Growth\')">SEO & Organic Growth</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Performance Marketing\')">Performance Marketing</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Branding & Creative\')">Branding & Creative</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Careers\')">Careers</button>' +
            '            <button class="ai-chat-quick-btn" onclick="sendQuickAction(\'Something Else\')">Something Else</button>' +
            '        </div>' +
            '    </div>' +
            '</div>' +
            '<!-- Input area -->' +
            '<div class="ai-chat-input-area">' +
            '    <input type="text" id="ai-chat-input-el" onkeydown="if(event.key===\'Enter\') sendChatMessage()" placeholder="Ask about services, pricing, stacks..." class="ai-chat-input">' +
            '    <button id="ai-send-btn" onclick="sendChatMessage()" class="ai-chat-send">' +
            '        <span class="material-symbols-outlined text-sm">send</span>' +
            '    </button>' +
            '</div>';

        var isBlogPage = window.location.pathname.indexOf('blog.html') !== -1;
        var chatbotBottomClass = isBlogPage ? 'bottom-[82px]' : 'bottom-8';
        var waBottomClass = isBlogPage ? 'bottom-[146px]' : 'bottom-24';

        var widgetEl = document.createElement('div');
        widgetEl.id = 'ai-agent-widget';
        widgetEl.className = 'ai-chat-window';
        if (isBlogPage) {
            widgetEl.style.bottom = '150px';
        }
        widgetEl.innerHTML = widgetHtml;
        document.body.appendChild(widgetEl);

        // 2. Reposition WhatsApp Button and Append AI Chat Toggle Button
        var waBtn = document.querySelector('a[href*="wa.me"]');
        var toggleBtn = document.createElement('button');
        toggleBtn.id = 'ai-agent-toggle-btn';
        toggleBtn.onclick = window.toggleAIAgent;
        toggleBtn.className = 'fixed ' + chatbotBottomClass + ' right-8 bg-[#3790ff] text-[#030816] w-14 h-14 rounded-full flex items-center justify-center shadow-lg hover:scale-110 hover:shadow-2xl transition-all duration-300 z-50 group border border-[#3790ff]/20 cursor-pointer';
        toggleBtn.setAttribute('aria-label', 'Toggle AI Chatbot');
        toggleBtn.innerHTML = '<svg style="width: 24px; height: 24px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; display: inline-block; vertical-align: middle;" viewBox="0 0 24 24">' +
            '                <rect x="3" y="11" width="18" height="10" rx="2"></rect>' +
            '                <circle cx="8.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '                <circle cx="15.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '                <path d="M10 19h4"></path>' +
            '                <path d="M12 6V11M12 3a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3z"></path>' +
            '                <path d="M3 14H1.5M21 14h1.5"></path>' +
            '            </svg>' +
            '<span class="absolute right-16 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">Chat with AI</span>';

        if (waBtn) {
            // Position the WhatsApp button just above the chatbot toggle button
            waBtn.classList.remove('bottom-8');
            waBtn.classList.remove('bottom-24');
            waBtn.classList.add(waBottomClass);
        } else {
            // If the page doesn't have it, create the WhatsApp button dynamically
            var newWaBtn = document.createElement('a');
            newWaBtn.href = 'https://wa.me/919990712555?text=Hello%20Blueshore%20Team,%20I\'d%20like%20to%20discuss%20a%20project.';
            newWaBtn.target = '_blank';
            newWaBtn.className = 'fixed ' + waBottomClass + ' right-8 bg-[#25D366] text-white w-14 h-14 rounded-full flex items-center justify-center shadow-lg hover:scale-110 hover:shadow-2xl transition-all duration-300 z-50 group';
            newWaBtn.innerHTML = '<svg class="w-8 h-8 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">' +
                '<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.489-1.761-1.662-2.061-.173-.299-.018-.461.13-.611.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>' +
                '</svg>' +
                '<span class="absolute right-16 bg-slate-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">Chat with us</span>';
            document.body.appendChild(newWaBtn);
        }

        document.body.appendChild(toggleBtn);

        // 4. Create and Append Global Support Hub
        var hubContainer = document.createElement('div');
        hubContainer.id = 'support-hub';
        hubContainer.innerHTML = 
            '<div id="support-hub-menu">' +
            '    <button class="hub-menu-btn hub-btn-ai" onclick="handleHubAIChat()" aria-label="Chat with AI">' +
            '        <span class="hub-tooltip">Chat with AI</span>' +
            '        <svg style="width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; display: inline-block; vertical-align: middle;" viewBox="0 0 24 24">' +
            '            <rect x="3" y="11" width="18" height="10" rx="2"></rect>' +
            '            <circle cx="8.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '            <circle cx="15.5" cy="16" r="1.5" fill="currentColor"></circle>' +
            '            <path d="M10 19h4"></path>' +
            '            <path d="M12 6V11M12 3a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3z"></path>' +
            '            <path d="M3 14H1.5M21 14h1.5"></path>' +
            '        </svg>' +
            '    </button>' +
            '    <a class="hub-menu-btn hub-btn-whatsapp" href="https://wa.me/919990712555?text=Hello%20Blueshore%20Team,%20I\'d%20like%20to%20discuss%20a%20project." target="_blank" rel="noopener" aria-label="WhatsApp Chat">' +
            '        <span class="hub-tooltip">WhatsApp Chat</span>' +
            '        <svg class="w-5 h-5 fill-current text-white" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:inline-block;vertical-align:middle;">' +
            '            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.489-1.761-1.662-2.061-.173-.299-.018-.461.13-.611.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/>' +
            '        </svg>' +
            '    </a>' +
            '</div>' +
            '<button id="support-hub-trigger" aria-label="Open contact and support menu">' +
            '    <span class="material-symbols-outlined text-2xl" id="hub-trigger-icon" style="font-variation-settings: \'FILL\' 0, \'wght\' 400, \'GRAD\' 0, \'opsz\' 24;">forum</span>' +
            '</button>';
        document.body.appendChild(hubContainer);

        var hubTrigger = document.getElementById('support-hub-trigger');
        var hubMenu = document.getElementById('support-hub-menu');
        var hubIcon = document.getElementById('hub-trigger-icon');

        if (hubTrigger && hubMenu) {
            hubTrigger.onclick = function(e) {
                e.stopPropagation();
                
                // If the AI chatbot is open, close it and open the hub menu
                var widget = document.getElementById('ai-agent-widget');
                if (widget && widget.classList.contains('active')) {
                    window.toggleAIAgent();
                    openHub();
                    return;
                }

                var isOpen = hubMenu.classList.contains('active');
                if (isOpen) {
                    closeHub();
                } else {
                    openHub();
                }
            };
        }

        window.handleHubAIChat = function() {
            closeHub();
            window.toggleAIAgent();
        };

        function openHub() {
            hubMenu.classList.add('active');
            hubTrigger.classList.add('active');
            if (hubIcon) hubIcon.textContent = 'close';
        }

        function closeHub() {
            hubMenu.classList.remove('active');
            hubTrigger.classList.remove('active');
            if (hubIcon) hubIcon.textContent = 'forum';
        }

        // Close hub when clicking outside
        document.addEventListener('click', function(e) {
            if (hubMenu && !hubMenu.contains(e.target) && e.target !== hubTrigger) {
                closeHub();
            }
        });

        // 3. Initialize Gemini Badges / Forms if Key is present
        // 3. Initialize Gemini Badges / Forms (Server-mediated by default)
        var badge = document.getElementById('ai-mode-badge');
        if (badge) {
            badge.textContent = '⚡ AI Powered';
            badge.className = 'ai-mode-badge ai-connected';
        }
    }

    /* ——————— Visitor Telemetry & WebSockets ——————— */
    var visitor_id = localStorage.getItem('blueshore-visitor-id') || '';
    if (!visitor_id) {
        visitor_id = 'vis_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        localStorage.setItem('blueshore-visitor-id', visitor_id);
    }

    var telemetrySocket = null;
    var currentChatMode = 'AI';
    var mouseBuffer = [];

    function getBrowserName() {
        var ua = navigator.userAgent;
        if (ua.indexOf("Chrome") > -1) return "Google Chrome";
        if (ua.indexOf("Firefox") > -1) return "Mozilla Firefox";
        if (ua.indexOf("Safari") > -1) return "Apple Safari";
        if (ua.indexOf("MSIE") > -1 || ua.indexOf("Trident/") > -1) return "Internet Explorer";
        if (ua.indexOf("Edge") > -1) return "Microsoft Edge";
        return "Browser";
    }

    function getOSName() {
        var pf = navigator.platform;
        if (pf.indexOf("Win") > -1) return "Windows";
        if (pf.indexOf("Mac") > -1) return "macOS";
        if (pf.indexOf("Linux") > -1) return "Linux";
        return "OS";
    }

    function getDeviceType() {
        var width = window.innerWidth;
        if (width < 768) return "Mobile";
        if (width < 1024) return "Tablet";
        return "Desktop";
    }

    function flushMouseBuffer() {
        if (telemetrySocket && telemetrySocket.readyState === WebSocket.OPEN && mouseBuffer.length > 0) {
            telemetrySocket.send(JSON.stringify({
                type: 'replay_frame',
                frames: mouseBuffer
            }));
            mouseBuffer = [];
        }
    }

    function initTelemetryListeners() {
        var lastScrollTime = 0;
        var lastScrollPct = 0;
        window.addEventListener('scroll', function () {
            var now = Date.now();
            if (now - lastScrollTime > 300) {
                var scrollPct = Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100) || 0;
                if (scrollPct !== lastScrollPct) {
                    lastScrollPct = scrollPct;
                    sendScrollUpdate(scrollPct);
                }
                lastScrollTime = now;
            }
        });

        var sections = document.querySelectorAll('section, header, footer, #contact-section');
        var activeSection = 'Hero';
        if ('IntersectionObserver' in window) {
            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        var id = entry.target.id;
                        if (!id) {
                            var heading = entry.target.querySelector('h1, h2, h3, h4');
                            if (heading && heading.textContent.trim()) {
                                id = heading.textContent.trim().substring(0, 30);
                            } else {
                                var tagName = entry.target.tagName.toLowerCase();
                                id = tagName.charAt(0).toUpperCase() + tagName.slice(1);
                            }
                        } else {
                            id = id.split(/[-_]/).map(function(word) {
                                if (!word) return '';
                                return word.charAt(0).toUpperCase() + word.slice(1);
                            }).join(' ');
                        }
                        
                        if (id && id !== 'Ai Agent Widget' && id !== 'Support Hub') {
                            activeSection = id;
                            sendScrollUpdate(lastScrollPct);
                        }
                    }
                });
            }, { threshold: 0.15 });
            sections.forEach(function (s) { observer.observe(s); });
        }

        function sendScrollUpdate(pct) {
            if (telemetrySocket && telemetrySocket.readyState === WebSocket.OPEN) {
                telemetrySocket.send(JSON.stringify({
                    type: 'scroll_update',
                    scroll_percentage: pct,
                    section: activeSection
                }));
            }
        }

        var lastMoveTime = 0;
        window.addEventListener('mousemove', function (e) {
            var now = Date.now();
            if (now - lastMoveTime > 150) {
                mouseBuffer.push({
                    x: e.clientX,
                    y: e.clientY,
                    sx: window.scrollX,
                    sy: window.scrollY,
                    t: now
                });
                lastMoveTime = now;
            }
        });

        window.addEventListener('click', function (e) {
            mouseBuffer.push({
                x: e.clientX,
                y: e.clientY,
                sx: window.scrollX,
                sy: window.scrollY,
                click: true,
                t: Date.now()
            });
        });

        var idleTimer = null;
        var isIdle = false;

        function resetIdleTimer() {
            if (isIdle) {
                isIdle = false;
                if (telemetrySocket && telemetrySocket.readyState === WebSocket.OPEN) {
                    telemetrySocket.send(JSON.stringify({
                        type: 'idle_update',
                        is_idle: false
                    }));
                }
            }
            if (idleTimer) clearTimeout(idleTimer);
            idleTimer = setTimeout(function () {
                isIdle = true;
                if (telemetrySocket && telemetrySocket.readyState === WebSocket.OPEN) {
                    telemetrySocket.send(JSON.stringify({
                        type: 'idle_update',
                        is_idle: true
                    }));
                }
            }, 60000);
        }

        window.addEventListener('mousemove', resetIdleTimer);
        window.addEventListener('keypress', resetIdleTimer);
        window.addEventListener('click', resetIdleTimer);
        window.addEventListener('scroll', resetIdleTimer);
        resetIdleTimer();
    }

    function updateHeaderBadge(mode) {
        var badge = document.getElementById('ai-mode-badge');
        if (!badge) return;
        if (mode === 'AI') {
            badge.textContent = '⚡ AI Powered';
            badge.className = 'ai-mode-badge ai-connected';
        } else if (mode === 'Human') {
            badge.textContent = '👤 Live Agent';
            badge.className = 'ai-mode-badge human-connected';
        } else if (mode === 'Hybrid') {
            badge.textContent = '🤖 Hybrid Mode';
            badge.className = 'ai-mode-badge hybrid-connected';
        }
    }

    function connectTelemetry() {
        var protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        var wsUrl = protocol + '//' + window.location.host + '/ws/intelligence/visitor/';
        
        telemetrySocket = new WebSocket(wsUrl);

        telemetrySocket.onopen = function () {
            console.log("Visitor telemetry connected");
            telemetrySocket.send(JSON.stringify({
                type: 'init',
                session_id: session_id,
                visitor_id: visitor_id,
                browser: getBrowserName(),
                device: getDeviceType(),
                os: getOSName(),
                screen_size: window.innerWidth + 'x' + window.innerHeight,
                referrer: document.referrer,
                current_url: window.location.href,
                page_title: document.title,
                first_visit: !localStorage.getItem('blueshore-visited-before'),
                is_returning: !!localStorage.getItem('blueshore-visited-before')
            }));
            localStorage.setItem('blueshore-visited-before', 'true');
            
            setInterval(flushMouseBuffer, 10000);
            initTelemetryListeners();
        };

        telemetrySocket.onmessage = function (event) {
            try {
                var data = JSON.parse(event.data);
                var type = data.type;

                if (type === 'mode_change') {
                    currentChatMode = data.chat_mode;
                    updateHeaderBadge(currentChatMode);
                } else if (type === 'chat_message') {
                    var msg = data.message;
                    appendAgentMessage(msg.text, msg.sender);
                    if (msg.proactive) {
                        var widget = document.getElementById('ai-agent-widget');
                        if (widget && !widget.classList.contains('active')) {
                            window.toggleAIAgent();
                        }
                    }
                } else if (type === 'typing_status') {
                    if (data.is_typing) {
                        showTyping();
                    } else {
                        removeTyping();
                    }
                }
            } catch (e) {
                console.error("Error processing telemetry packet", e);
            }
        };

        telemetrySocket.onclose = function () {
            console.log("Telemetry socket closed, reconnecting...");
            setTimeout(connectTelemetry, 5000);
        };
    }

    // Run injection and connect telemetry when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            injectChatbot();
            connectTelemetry();
        });
    } else {
        injectChatbot();
        connectTelemetry();
    }
})();

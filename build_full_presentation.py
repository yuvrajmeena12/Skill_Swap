import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

# ---------------------------------------------------------------------------
# COLOR PALETTE & STYLING CONSTANTS (Matched directly from user templates)
# ---------------------------------------------------------------------------
MAROON_BANNER = RGBColor(155, 41, 49)      # #9B2931 Title bar
RED_FOOTER = RGBColor(185, 28, 28)         # #B91C1C Footer bar
DARK_TEXT = RGBColor(25, 30, 36)           # Deep charcoal for body
WHITE = RGBColor(255, 255, 255)
LIGHT_BG = RGBColor(248, 250, 252)         # Off-white card background
CARD_BORDER = RGBColor(226, 232, 240)      # Subtle gray border
ACCENT_BLUE = RGBColor(14, 116, 144)       # Teal/cyan accent
ACCENT_INDIGO = RGBColor(79, 70, 229)      # Indigo accent

ASSETS_DIR = r"c:\Users\GANPATI\OneDrive\Documents\SKILL_SWAP_FSD\ppt_assets"
SKIT_LOGO = os.path.join(ASSETS_DIR, "skit_logo.png")
SWAMI_IMG = os.path.join(ASSETS_DIR, "swami_portrait.png")
TECH_LOGOS = os.path.join(ASSETS_DIR, "tech_stack_logos.png")
SCREEN_HOME = os.path.join(ASSETS_DIR, "screen_home.png")
SCREEN_REG = os.path.join(ASSETS_DIR, "screen_register.png")
SCREEN_LOGIN = os.path.join(ASSETS_DIR, "screen_login.png")

prs = Presentation()
# Set widescreen 16:9 (13.333 x 7.5 inches)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def apply_transition(slide):
    """Adds a smooth fade transition between slides."""
    try:
        tr_xml = parse_xml('<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>')
        slide._element.append(tr_xml)
    except Exception:
        pass

def add_header_footer(slide, title_text):
    """Renders the exact template header & footer on content slides."""
    apply_transition(slide)

    # 1. SKIT Logo (Top Left)
    if os.path.exists(SKIT_LOGO):
        slide.shapes.add_picture(SKIT_LOGO, Inches(0.35), Inches(0.2), width=Inches(1.25), height=Inches(1.25))

    # 2. Maroon Title Banner (Exact match to template)
    title_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.85), Inches(0.35), Inches(11.1), Inches(0.95))
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = MAROON_BANNER
    title_box.line.color.rgb = RGBColor(30, 20, 20)
    title_box.line.width = Pt(1.5)

    tf = title_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # 3. Red Footer Bar (Exact match to template)
    footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.05), Inches(13.333), Inches(0.45))
    footer_bar.fill.solid()
    footer_bar.fill.fore_color.rgb = RED_FOOTER
    footer_bar.line.fill.background()

    # Footer Left: SKIT, JAIPUR
    tx_left = slide.shapes.add_textbox(Inches(0.4), Inches(7.08), Inches(3.0), Inches(0.35))
    tf_l = tx_left.text_frame
    tf_l.word_wrap = False
    p_l = tf_l.paragraphs[0]
    p_l.text = "SKIT, JAIPUR"
    p_l.font.name = "Arial"
    p_l.font.size = Pt(11)
    p_l.font.bold = True
    p_l.font.color.rgb = WHITE

    # Footer Center: www.skit.ac.in
    tx_center = slide.shapes.add_textbox(Inches(5.0), Inches(7.08), Inches(3.33), Inches(0.35))
    tf_c = tx_center.text_frame
    tf_c.word_wrap = False
    p_c = tf_c.paragraphs[0]
    p_c.text = "www.skit.ac.in"
    p_c.font.name = "Arial"
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = WHITE
    p_c.alignment = PP_ALIGN.CENTER

# ===========================================================================
# SLIDE 1: TITLE SLIDE (Exact match to Image 3)
# ===========================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_transition(s1)

# Logos
if os.path.exists(SKIT_LOGO):
    s1.shapes.add_picture(SKIT_LOGO, Inches(0.35), Inches(0.2), width=Inches(1.3), height=Inches(1.3))
if os.path.exists(SWAMI_IMG):
    s1.shapes.add_picture(SWAMI_IMG, Inches(11.7), Inches(0.18), width=Inches(1.2), height=Inches(1.35))

# Top College Name (Serif, Red/Maroon)
top_tx = s1.shapes.add_textbox(Inches(1.8), Inches(0.3), Inches(9.7), Inches(1.2))
tf = top_tx.text_frame
tf.word_wrap = True
p1 = tf.paragraphs[0]
p1.text = "Swami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
p1.font.name = "Georgia"
p1.font.size = Pt(20)
p1.font.bold = True
p1.font.color.rgb = RGBColor(160, 30, 30)
p1.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = "(An Autonomous Institute Affiliated to Rajasthan Technical University, Kota)"
p2.font.name = "Georgia"
p2.font.size = Pt(15)
p2.font.bold = True
p2.font.color.rgb = RGBColor(160, 30, 30)
p2.alignment = PP_ALIGN.CENTER

# Main Title Section
center_tx = s1.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.33), Inches(2.4))
tf_c = center_tx.text_frame
tf_c.word_wrap = True

p_it = tf_c.paragraphs[0]
p_it.text = "Industrial Training"
p_it.font.name = "Georgia"
p_it.font.size = Pt(32)
p_it.font.bold = True
p_it.font.color.rgb = DARK_TEXT
p_it.alignment = PP_ALIGN.CENTER

p_pr = tf_c.add_paragraph()
p_pr.text = "Presentation"
p_pr.font.name = "Georgia"
p_pr.font.size = Pt(32)
p_pr.font.bold = True
p_pr.font.color.rgb = DARK_TEXT
p_pr.alignment = PP_ALIGN.CENTER
p_pr.space_after = Pt(24)

p_top = tf_c.add_paragraph()
p_top.text = "TOPIC: Skill Swap"
p_top.font.name = "Arial Black"
p_top.font.size = Pt(38)
p_top.font.bold = True
p_top.font.underline = True
p_top.font.color.rgb = RGBColor(17, 24, 39)
p_top.alignment = PP_ALIGN.CENTER

# Bottom Meta Section
# Left: Submitted To
sub_to = s1.shapes.add_textbox(Inches(0.8), Inches(5.2), Inches(5.0), Inches(1.5))
tf_to = sub_to.text_frame
tf_to.word_wrap = True

p = tf_to.paragraphs[0]
p.text = "Submitted To:"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

p = tf_to.add_paragraph()
p.text = "Name:- Mr. Vikash Dhankar"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

p = tf_to.add_paragraph()
p.text = "Assistant Professor"
p.font.name = "Arial"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

# Right: Submitted By & Organization
sub_by = s1.shapes.add_textbox(Inches(7.5), Inches(5.0), Inches(5.2), Inches(1.8))
tf_by = sub_by.text_frame
tf_by.word_wrap = True

p = tf_by.paragraphs[0]
p.text = "Organization: N code labs"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_TEXT
p.space_after = Pt(10)

p = tf_by.add_paragraph()
p.text = "Submitted By:"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

p = tf_by.add_paragraph()
p.text = "Name:- Yuvraj Meena (24ESKCS780)"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

# Footer Bar on Slide 1
footer_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.05), Inches(13.333), Inches(0.45))
footer_bar.fill.solid()
footer_bar.fill.fore_color.rgb = RED_FOOTER
footer_bar.line.fill.background()

tx_left = s1.shapes.add_textbox(Inches(0.4), Inches(7.08), Inches(3.0), Inches(0.35))
tx_left.text_frame.paragraphs[0].text = "SKIT, JAIPUR"
tx_left.text_frame.paragraphs[0].font.size = Pt(11)
tx_left.text_frame.paragraphs[0].font.bold = True
tx_left.text_frame.paragraphs[0].font.color.rgb = WHITE

tx_center = s1.shapes.add_textbox(Inches(5.0), Inches(7.08), Inches(3.33), Inches(0.35))
tx_center.text_frame.paragraphs[0].text = "www.skit.ac.in"
tx_center.text_frame.paragraphs[0].font.size = Pt(11)
tx_center.text_frame.paragraphs[0].font.bold = True
tx_center.text_frame.paragraphs[0].font.color.rgb = WHITE
tx_center.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER


# ===========================================================================
# SLIDE 2: INDEX (Exact match to Image 2)
# ===========================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header_footer(s2, "Index")

idx_box = s2.shapes.add_textbox(Inches(2.5), Inches(1.7), Inches(9.0), Inches(5.0))
tf = idx_box.text_frame
tf.word_wrap = True

index_items = [
    "1. Company Introduction",
    "2. Certificate",
    "3. Technology Used",
    "4. Goal of Training",
    "5. Project Overview",
    "6. Working Project",
    "7. Future Scope",
    "8. Q&A"
]

for i, item in enumerate(index_items):
    p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
    p.text = item
    p.font.name = "Arial"
    p.font.size = Pt(26)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(14)


# ===========================================================================
# SLIDE 3: COMPANY INTRODUCTION (Reserved Page)
# ===========================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header_footer(s3, "Company Introduction")

frame3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.8), Inches(10.33), Inches(4.8))
frame3.fill.solid()
frame3.fill.fore_color.rgb = LIGHT_BG
frame3.line.color.rgb = RGBColor(180, 190, 205)
frame3.line.width = Pt(2)

tf3 = frame3.text_frame
tf3.word_wrap = True
tf3.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf3.paragraphs[0]
p.text = "[ COMPANY PROFILE & BACKGROUND ]"
p.font.name = "Arial"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = MAROON_BANNER
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(16)

p = tf3.add_paragraph()
p.text = "This slide is designated for organization details, industrial background, and training domain overview."
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(100, 116, 139)
p.alignment = PP_ALIGN.CENTER

p = tf3.add_paragraph()
p.text = "(Paste company overview text, leadership, client portfolios, or corporate brochure screenshot here)"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.italic = True
p.font.color.rgb = RGBColor(148, 163, 184)
p.alignment = PP_ALIGN.CENTER


# ===========================================================================
# SLIDE 4: CERTIFICATE (Reserved Page)
# ===========================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header_footer(s4, "Certificate")

frame4 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.8), Inches(10.33), Inches(4.8))
frame4.fill.solid()
frame4.fill.fore_color.rgb = LIGHT_BG
frame4.line.color.rgb = RGBColor(180, 190, 205)
frame4.line.width = Pt(2)

tf4 = frame4.text_frame
tf4.word_wrap = True
tf4.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf4.paragraphs[0]
p.text = "[ INDUSTRIAL TRAINING CERTIFICATE ]"
p.font.name = "Arial"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = MAROON_BANNER
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(16)

p = tf4.add_paragraph()
p.text = "Space reserved for training completion certificate awarded by the organization."
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.color.rgb = RGBColor(100, 116, 139)
p.alignment = PP_ALIGN.CENTER

p = tf4.add_paragraph()
p.text = "(Insert scanned certificate image or authorized letter of completion here)"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.italic = True
p.font.color.rgb = RGBColor(148, 163, 184)
p.alignment = PP_ALIGN.CENTER


# ===========================================================================
# SLIDE 5: TECHNOLOGY USED (Tech Stack with Real Logos)
# ===========================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header_footer(s5, "Tech Stack")

# Add the real logos extracted from the user's template
if os.path.exists(TECH_LOGOS):
    s5.shapes.add_picture(TECH_LOGOS, Inches(2.2), Inches(1.5), width=Inches(8.93), height=Inches(4.1))

# Category descriptions at the bottom
desc_box = s5.shapes.add_textbox(Inches(1.2), Inches(5.7), Inches(10.9), Inches(1.1))
tf5 = desc_box.text_frame
tf5.word_wrap = True

p = tf5.paragraphs[0]
p.text = "• Frontend Layer: React.js (Component Architecture), Tailwind CSS (Modern Glassmorphic UI), Vite (Build Tool), Axios (HTTP Client)"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

p = tf5.add_paragraph()
p.text = "• Backend & APIs: Node.js (V8 Engine Runtime), Express.js (REST Routing), JWT (Encrypted Auth), Multer (File Handling)"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_TEXT

p = tf5.add_paragraph()
p.text = "• Database & Storage: MongoDB Atlas (Mongoose ODM, Replica Sets), Cloudinary (Cloud Media CDN for Profiles & Proofs)"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = DARK_TEXT


# ===========================================================================
# SLIDE 6: GOAL OF TRAINING (Exact match to Image 1)
# ===========================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header_footer(s6, "Goal of Training")

goals_box = s6.shapes.add_textbox(Inches(1.8), Inches(1.7), Inches(10.2), Inches(5.0))
tfg = goals_box.text_frame
tfg.word_wrap = True

goals_data = [
    ("Learn practical ", "Full-Stack Web Development", " (MERN Stack architecture)"),
    ("Understand ", "React frontend development", " with reusable components & hooks"),
    ("Develop ", "Node.js & Express backend APIs", " with token security & validation"),
    ("Work with ", "MongoDB and Cloudinary", " for scalable database schemas & media"),
    ("Design ", "algorithmic peer-to-peer matching", " for reciprocal skill swaps"),
    ("Implement ", "secure authentication workflows", " using JWT & dual verification"),
    ("Gain experience in building a ", "complete real-world project", " from scratch to deployment")
]

for i, (pre, bold_text, post) in enumerate(goals_data):
    p = tfg.add_paragraph() if i > 0 else tfg.paragraphs[0]
    p.space_after = Pt(18)
    
    # Bullet symbol
    r0 = p.add_run()
    r0.text = "• "
    r0.font.name = "Arial"
    r0.font.size = Pt(22)
    r0.font.bold = True
    r0.font.color.rgb = DARK_TEXT

    r1 = p.add_run()
    r1.text = pre
    r1.font.name = "Arial"
    r1.font.size = Pt(22)
    r1.font.color.rgb = DARK_TEXT

    r2 = p.add_run()
    r2.text = bold_text
    r2.font.name = "Arial"
    r2.font.size = Pt(22)
    r2.font.bold = True
    r2.font.color.rgb = DARK_TEXT

    r3 = p.add_run()
    r3.text = post
    r3.font.name = "Arial"
    r3.font.size = Pt(22)
    r3.font.color.rgb = DARK_TEXT


# ===========================================================================
# SLIDE 7: PROJECT OVERVIEW (Problem & Solution)
# ===========================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header_footer(s7, "Project Overview")

# Left Card: Problem Statement
card_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.7), Inches(5.2), Inches(4.9))
card_l.fill.solid()
card_l.fill.fore_color.rgb = LIGHT_BG
card_l.line.color.rgb = CARD_BORDER
card_l.line.width = Pt(1.5)

tf_l = card_l.text_frame
tf_l.word_wrap = True
p = tf_l.paragraphs[0]
p.text = "⚠️ The Problem Statement"
p.font.name = "Arial"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = MAROON_BANNER
p.space_after = Pt(14)

probs = [
    "High Cost of Tutoring: Millions possess valuable skills (programming, languages, design) but lack funds for paid courses or coaching.",
    "Monetization Barriers: Monetizing talent requires formal freelance platforms with steep platform commissions (20%+).",
    "Underutilized Knowledge: Peer learning remains fragmented across informal social networks with no accountability or structure."
]
for prob in probs:
    p = tf_l.add_paragraph()
    p.text = "• " + prob
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(10)

# Right Card: The SkillSwap Solution
card_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.7), Inches(5.2), Inches(4.9))
card_r.fill.solid()
card_r.fill.fore_color.rgb = LIGHT_BG
card_r.line.color.rgb = CARD_BORDER
card_r.line.width = Pt(1.5)

tf_r = card_r.text_frame
tf_r.word_wrap = True
p = tf_r.paragraphs[0]
p.text = "💡 The SkillSwap Solution"
p.font.name = "Arial"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO
p.space_after = Pt(14)

sols = [
    "Barter Economy for Knowledge: A direct peer-to-peer exchange where members trade skills without any financial transaction.",
    "Two-Way Reciprocal Matching: Smart algorithm matches users where 'Skill Offered by A' equals 'Skill Wanted by B' and vice-versa.",
    "Built-in Coordination Lifecycle: End-to-end request management, session scheduling, verified proof badges, and mutual reviews."
]
for sol in sols:
    p = tf_r.add_paragraph()
    p.text = "• " + sol
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(10)


# ===========================================================================
# SLIDE 8: WORKING PROJECT - SYSTEM ARCHITECTURE & FLOW
# ===========================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header_footer(s8, "Working Project: System Architecture")

steps = [
    ("1. Auth & Profiles", "Secure signup with OTP verification, profile customization, and bio setup."),
    ("2. Skill Catalog", "List skills under 'I Can Teach' & 'I Want to Learn' with levels & modalities."),
    ("3. Smart Match Engine", "Algorithmic discovery pairing mutual reciprocal skill requirements."),
    ("4. Swap Proposal", "Send 1-on-1 swap offers with customized introductory negotiation messages."),
    ("5. Session Coordination", "Schedule dates, choose online meeting links or in-person venues."),
    ("6. Reviews & Trust Score", "Mark completed, submit 1-5 star ratings, and earn verified status.")
]

for idx, (title, desc) in enumerate(steps):
    col = idx % 3
    row = idx // 3
    x = Inches(1.2 + col * 3.8)
    y = Inches(1.8 + row * 2.5)

    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.5), Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BG
    card.line.color.rgb = RGBColor(203, 213, 225)
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = MAROON_BANNER
    p.space_after = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.color.rgb = DARK_TEXT


# ===========================================================================
# SLIDE 9: WORKING PROJECT - LANDING PAGE & DISCOVERY (With Real Screenshot)
# ===========================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header_footer(s9, "Working Project: Landing Page & UX")

# Insert real screenshot of homepage
if os.path.exists(SCREEN_HOME):
    s9.shapes.add_picture(SCREEN_HOME, Inches(1.0), Inches(1.7), width=Inches(6.6), height=Inches(4.9))

# Explanation panel on the right
panel = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.7), Inches(4.5), Inches(4.9))
panel.fill.solid()
panel.fill.fore_color.rgb = LIGHT_BG
panel.line.color.rgb = CARD_BORDER

tf = panel.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Features & Interface Functions"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO
p.space_after = Pt(12)

bullets = [
    "Contemporary Glassmorphic Theme: Deep midnight aesthetic with glowing cyan accents and accessible typography.",
    "Value Proposition Display: Immediate clarity with 'Teach What You Know. Master What You Want' hero messaging.",
    "Interactive Barter Paradigm: Demonstrates real-time 1-to-1 reciprocity exchange tickets directly on the home feed.",
    "Public Directory Preview: Non-logged in visitors can browse public skill offerings with instant search capability.",
    "Direct Call to Action: Seamless onboarding flow directing users into registration or passwordless login."
]
for b in bullets:
    p = tf.add_paragraph()
    p.text = "✔ " + b
    p.font.name = "Arial"
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(8)


# ===========================================================================
# SLIDE 10: WORKING PROJECT - AUTHENTICATION & SECURITY (With Real Screenshot)
# ===========================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header_footer(s10, "Working Project: Auth & Security")

# Embed real screenshot of registration/login
if os.path.exists(SCREEN_REG):
    s10.shapes.add_picture(SCREEN_REG, Inches(1.0), Inches(1.7), width=Inches(6.6), height=Inches(4.9))

panel10 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.7), Inches(4.5), Inches(4.9))
panel10.fill.solid()
panel10.fill.fore_color.rgb = LIGHT_BG
panel10.line.color.rgb = CARD_BORDER

tf = panel10.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Security Architecture & Controls"
p.font.name = "Arial"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = MAROON_BANNER
p.space_after = Pt(12)

sec_bullets = [
    "Dual Authentication Channels: Supports both classic encrypted passwords and instantaneous Email OTP verification.",
    "Mandatory Verification Checks: Form validation enforces RFC-compliant emails, 10-15 digit phone numbers, and min 6-char passwords.",
    "Encrypted JWT Sessions: Issues JSON Web Tokens stored securely with 30-day expiry and automated HTTP Authorization headers.",
    "Password Protection: Utilizes bcrypt with cryptographic salt rounds to prevent rainbow table and brute-force attacks.",
    "Rate Limiting & Safety: OTP attempts throttled with dynamic 60-second cool-downs to block spamming."
]
for b in sec_bullets:
    p = tf.add_paragraph()
    p.text = "🔒 " + b
    p.font.name = "Arial"
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_TEXT
    p.space_after = Pt(8)


# ===========================================================================
# SLIDE 11: WORKING PROJECT - CORE MODULES & FEATURES
# ===========================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header_footer(s11, "Working Project: Core Modules")

features = [
    ("Skill Management System", [
        "Dual taxonomy: 'I Can Teach' vs. 'I Want to Learn'",
        "Categorization: Tech, Music, Language, Fitness, Art, Cooking, Academic",
        "Proficiency levels: Beginner, Intermediate, Expert",
        "Modality configuration: Online, In-person, or Both"
    ]),
    ("Smart Match & Barter Engine", [
        "Dynamic reciprocal query engine matching complementary skills",
        "Mutual Match Badge: Instant visual indicator for 2-way compatibility",
        "Direct proposal modal selecting exact skills to trade",
        "Introductory message thread attached to incoming proposals"
    ]),
    ("Session Coordination & Chat", [
        "Proposal negotiation: Accept, Decline, or Counter-propose",
        "Session scheduling: Date picker, time slots, and virtual meeting links",
        "Real-time messaging per active swap transaction",
        "Two-party confirmation locking in scheduled dates"
    ]),
    ("Trust, Reviews & Badges", [
        "Mandatory swap completion confirmation by both learners",
        "1 to 5 star rating system with detailed qualitative feedback",
        "Dynamic Trust Score algorithm displayed publicly on user profiles",
        "Verified Member Badge unlocked after 5 verified swaps"
    ])
]

for idx, (title, items) in enumerate(features):
    col = idx % 2
    row = idx // 2
    x = Inches(1.2 + col * 5.6)
    y = Inches(1.8 + row * 2.5)

    card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.3), Inches(2.25))
    card.fill.solid()
    card.fill.fore_color.rgb = LIGHT_BG
    card.line.color.rgb = CARD_BORDER

    tf = card.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = MAROON_BANNER
    p.space_after = Pt(4)

    for item in items:
        p2 = tf.add_paragraph()
        p2.text = "• " + item
        p2.font.name = "Arial"
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = DARK_TEXT


# ===========================================================================
# SLIDE 12: FUTURE SCOPE
# ===========================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header_footer(s12, "Future Scope")

future_items = [
    ("🤖 AI-Powered Smart Matchmaking", 
     "Integrate vector embeddings (LangChain + Gemini / Groq) to perform semantic matching based on syllabus content and user learning goals rather than exact keyword matches."),
    ("📹 Integrated WebRTC Video Classrooms", 
     "Build built-in audio/video calling with screen sharing directly inside SkillSwap, eliminating the need to redirect to external Zoom or Google Meet links."),
    ("🔄 Multi-Party Circular Barter Swaps", 
     "Implement circular matching algorithms (3-way or 4-way trades: User A teaches User B, User B teaches User C, and User C teaches User A) when direct 2-way swaps aren't available."),
    ("📱 Native Mobile Application (React Native)", 
     "Develop cross-platform iOS and Android applications with geolocation-based campus matching and push notifications for instant session coordination."),
    ("🏆 Gamified Learning Streaks & Badges", 
     "Introduce learning milestone badges, community leaderboards, and peer-endorsed certificates to foster long-term student engagement and accountability.")
]

f_box = s12.shapes.add_textbox(Inches(1.5), Inches(1.6), Inches(10.5), Inches(5.2))
tf12 = f_box.text_frame
tf12.word_wrap = True

for idx, (title, desc) in enumerate(future_items):
    p = tf12.add_paragraph() if idx > 0 else tf12.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = MAROON_BANNER

    p_desc = tf12.add_paragraph()
    p_desc.text = desc
    p_desc.font.name = "Arial"
    p_desc.font.size = Pt(13.5)
    p_desc.font.color.rgb = DARK_TEXT
    p_desc.space_after = Pt(10)


# ===========================================================================
# SLIDE 13: Q&A (Concluding Slide)
# ===========================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header_footer(s13, "Q & A")

qa_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(2.0), Inches(8.33), Inches(4.3))
qa_card.fill.solid()
qa_card.fill.fore_color.rgb = LIGHT_BG
qa_card.line.color.rgb = CARD_BORDER
qa_card.line.width = Pt(2)

tf13 = qa_card.text_frame
tf13.word_wrap = True
tf13.vertical_anchor = MSO_ANCHOR.MIDDLE

p = tf13.paragraphs[0]
p.text = "Thank You!"
p.font.name = "Georgia"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = MAROON_BANNER
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(14)

p = tf13.add_paragraph()
p.text = "Any Questions or Suggestions?"
p.font.name = "Arial"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = DARK_TEXT
p.alignment = PP_ALIGN.CENTER
p.space_after = Pt(20)

p = tf13.add_paragraph()
p.text = "Project: Skill Swap (Full-Stack Peer Skill Exchange Platform)\nCandidate: Yuvraj Meena (Roll No: 24ESKCS780)\nDepartment of Computer Science & Engineering\nSwami Keshvanand Institute of Technology, Management & Gramothan, Jaipur"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.color.rgb = RGBColor(71, 85, 105)
p.alignment = PP_ALIGN.CENTER


# Save presentation
output_pptx = r"c:\Users\GANPATI\OneDrive\Documents\SKILL_SWAP_FSD\Skill_Swap_Presentation.pptx"
prs.save(output_pptx)
print(f"Full presentation generated successfully at: {output_pptx}")

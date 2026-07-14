import json
from datetime import datetime, timedelta

SITE_CONFIG = {
    "site_name": "Hearing Aids Veterans Guide",
    "site_url": "https://hearing-aids-veterans.bongshai.com",
    "author_name": "Dr. Sarah Mitchell, Audiologist & Veterans Advocate",
    "author_bio": "Dr. Sarah Mitchell has over 15 years of experience in audiology, specializing in helping US military veterans navigate VA benefits and find the right hearing solutions.",
    "contact_email": "contact@hearing-aids-veterans.bongshai.com",
    "description": "The definitive guide for US veterans seeking information on hearing aids, VA benefits, and audiology care.",
    "theme_color": "#0d47a1"
}

CATEGORIES = {
    "va-benefits": {
        "title": "VA Benefits & Coverage",
        "description": "Understand how to navigate the Veterans Affairs system to get coverage for your hearing aids."
    },
    "choosing-hearing-aids": {
        "title": "Choosing Hearing Aids",
        "description": "Comprehensive guides to selecting the best hearing aid models, styles, and technologies for your lifestyle."
    },
    "hearing-loss-types": {
        "title": "Types of Hearing Loss",
        "description": "Learn about tinnitus, noise-induced hearing loss, and other conditions common among military veterans."
    },
    "care-and-maintenance": {
        "title": "Care & Maintenance",
        "description": "Tips on how to clean, maintain, and troubleshoot your hearing aids to ensure longevity."
    }
}

raw_articles = [
    ("How to Get Hearing Aids Through the VA", "va-benefits", "how-to-get-hearing-aids-through-va", "A complete step-by-step guide for veterans to apply for and receive fully funded hearing aids through the Department of Veterans Affairs.", "VA hearing aids process"),
    ("Does the VA Cover Tinnitus Treatment?", "va-benefits", "va-tinnitus-treatment-coverage", "Find out if the VA covers tinnitus treatment, masking devices, and therapies for veterans suffering from ringing in the ears.", "VA tinnitus coverage"),
    ("Top 5 Hearing Aids Recommended for Veterans in 2024", "choosing-hearing-aids", "top-5-hearing-aids-veterans", "Discover the best hearing aid models currently offered and recommended by audiologists for military veterans.", "best hearing aids for veterans"),
    ("VA Disability Rating for Hearing Loss Explained", "va-benefits", "va-disability-rating-hearing-loss", "Understand how the VA calculates disability ratings for noise-induced hearing loss and what it means for your compensation.", "VA hearing loss rating"),
    ("Bluetooth Hearing Aids vs. Standard: What Should Veterans Choose?", "choosing-hearing-aids", "bluetooth-vs-standard-hearing-aids", "Compare Bluetooth-enabled hearing aids with standard models to decide which fits your lifestyle and communication needs.", "bluetooth hearing aids veterans"),
    ("How to Clean and Maintain Your VA Issued Hearing Aids", "care-and-maintenance", "clean-maintain-va-hearing-aids", "Learn the daily and weekly maintenance routines required to keep your VA-issued hearing aids in perfect working condition.", "cleaning hearing aids"),
    ("Understanding Service-Connected Hearing Loss", "hearing-loss-types", "service-connected-hearing-loss", "Explore the definition of service-connected hearing loss, its common causes in the military, and how to prove your claim.", "service-connected hearing loss"),
    ("Can You Upgrade Your VA Hearing Aids?", "va-benefits", "upgrade-va-hearing-aids", "Are you stuck with older models? Learn how and when veterans can request an upgrade for their VA hearing aids.", "upgrade VA hearing aids"),
    ("Invisible Hearing Aids: Are They Available Through the VA?", "choosing-hearing-aids", "invisible-hearing-aids-va", "Find out if completely-in-canal (CIC) or invisible hearing aids are an option for veterans receiving VA healthcare.", "invisible hearing aids VA"),
    ("The Link Between PTSD and Tinnitus in Veterans", "hearing-loss-types", "ptsd-and-tinnitus-veterans", "Research shows a strong connection between PTSD and tinnitus. Read about how these conditions interact and treatment options.", "PTSD and tinnitus"),
    ("How Long Do Hearing Aid Batteries Last?", "care-and-maintenance", "how-long-hearing-aid-batteries-last", "A guide to understanding hearing aid battery life, rechargeable vs. disposable options, and tips to extend battery longevity.", "hearing aid battery life"),
    ("Rechargeable Hearing Aids vs. Disposable Batteries", "choosing-hearing-aids", "rechargeable-vs-disposable-hearing-aids", "Weighing the pros and cons of rechargeable hearing aids against traditional disposable battery models for veterans.", "rechargeable hearing aids"),
    ("What to Expect at Your First VA Audiology Appointment", "va-benefits", "first-va-audiology-appointment", "Nervous about your first hearing test at the VA? Here is a breakdown of what happens during a standard audiology exam.", "VA audiology appointment"),
    ("Over-the-Counter (OTC) Hearing Aids vs. Prescription (VA)", "choosing-hearing-aids", "otc-vs-prescription-hearing-aids", "Are OTC hearing aids a good alternative for veterans? Compare them with the prescription devices provided by the VA.", "OTC hearing aids"),
    ("How to Appeal a Denied VA Claim for Hearing Loss", "va-benefits", "appeal-denied-va-claim-hearing-loss", "Was your claim for hearing loss denied? Learn the steps to file an appeal and get the VA benefits you deserve.", "appeal VA hearing loss claim"),
    ("Noise-Induced Hearing Loss from Military Firearms", "hearing-loss-types", "noise-induced-hearing-loss-firearms", "Examining how exposure to military firearms causes irreversible noise-induced hearing loss and how to seek help.", "firearm hearing loss military"),
    ("Troubleshooting Common Hearing Aid Problems", "care-and-maintenance", "troubleshooting-hearing-aid-problems", "Is your hearing aid whistling, distorted, or dead? Follow this troubleshooting guide to fix common issues at home.", "troubleshoot hearing aid"),
    ("Does Medicare Cover Hearing Aids for Veterans?", "va-benefits", "medicare-hearing-aids-coverage", "Clarifying the confusion around Medicare coverage for hearing aids and why veterans should use their VA benefits instead.", "Medicare hearing aids"),
    ("The Best Hearing Aid Accessories for Veterans", "choosing-hearing-aids", "best-hearing-aid-accessories", "Enhance your hearing experience with these top accessories, from TV streamers to remote microphones, available to veterans.", "hearing aid accessories"),
    ("Understanding the VA Audiology Community Care Program", "va-benefits", "va-audiology-community-care", "Wait times too long at your local VA? Learn how to use the Community Care program to see a private audiologist.", "VA Community Care audiology"),
    ("Signs You Might Need Hearing Aids", "hearing-loss-types", "signs-you-need-hearing-aids", "Not sure if your hearing has declined? Look out for these early warning signs of hearing loss common in older veterans.", "signs of hearing loss"),
    ("How to Dry Wet Hearing Aids Safely", "care-and-maintenance", "dry-wet-hearing-aids", "Accidentally wore your hearing aids in the shower? Step-by-step instructions on how to dry them out safely without causing damage.", "wet hearing aids"),
    ("Phonak vs. ReSound: Which is Better for Veterans?", "choosing-hearing-aids", "phonak-vs-resound-veterans", "A detailed comparison of two leading hearing aid brands frequently dispensed by the VA: Phonak and ReSound.", "Phonak vs ReSound"),
    ("What is a C&P Exam for Hearing Loss?", "va-benefits", "cp-exam-hearing-loss", "Everything you need to know about the Compensation and Pension (C&P) exam for hearing loss and tinnitus.", "C&P exam hearing loss"),
    ("Coping with Tinnitus: Maskers, Apps, and Therapies", "hearing-loss-types", "coping-with-tinnitus", "Discover effective strategies, sound maskers, and mobile apps designed to help veterans cope with severe tinnitus.", "tinnitus relief veterans"),
    ("Replacing Lost or Damaged VA Hearing Aids", "va-benefits", "replacing-lost-va-hearing-aids", "Lost your hearing aids? Find out the VA's policy on replacing lost, stolen, or accidentally damaged hearing devices.", "replace lost VA hearing aids"),
    ("How to Read Your Audiogram", "hearing-loss-types", "how-to-read-audiogram", "Learn how to interpret your audiogram test results and understand what the decibel and frequency numbers mean.", "read audiogram"),
    ("Are Custom Ear Molds Better Than Domes?", "choosing-hearing-aids", "custom-ear-molds-vs-domes", "Explore the differences between custom-fit ear molds and standard silicone domes for optimal hearing aid comfort.", "ear molds vs domes"),
    ("Traveling with Hearing Aids: Tips for Veterans", "care-and-maintenance", "traveling-with-hearing-aids", "Essential tips for packing, passing through TSA security, and maintaining your hearing aids while traveling.", "traveling with hearing aids"),
    ("The Impact of Untreated Hearing Loss on Cognitive Health", "hearing-loss-types", "untreated-hearing-loss-cognitive-health", "Why treating hearing loss early is crucial for preventing cognitive decline, isolation, and dementia in aging veterans.", "hearing loss and dementia"),
    ("How to Pair Your Bluetooth Hearing Aids to Your Smartphone", "care-and-maintenance", "pair-bluetooth-hearing-aids-smartphone", "A quick and easy guide to connecting your modern Bluetooth hearing aids to iPhones and Android devices.", "pair hearing aids phone"),
    ("VA Benefits for Spouses of Veterans with Hearing Loss", "va-benefits", "va-benefits-spouses-hearing-loss", "Learn what support, if any, is available for the spouses and dependents of veterans suffering from profound hearing loss.", "VA benefits spouse")
]

import random

states_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", 
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", 
    "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
]

for st in states_list:
    raw_articles.append((f"VA Audiology Clinics and Resources in {st}", "va-benefits", f"va-audiology-clinics-{st.lower().replace(' ', '-')}", f"A complete guide to finding VA audiology clinics and hearing aid resources for veterans in {st}.", f"VA audiology {st}"))
    raw_articles.append((f"State Assistance for Veterans Hearing Aids in {st}", "va-benefits", f"state-assistance-hearing-aids-{st.lower().replace(' ', '-')}", f"Learn about additional state-level assistance programs for veterans seeking hearing aids in {st}.", f"veterans hearing aids {st}"))
    raw_articles.append((f"Finding Veteran-Friendly Audiologists in {st}", "choosing-hearing-aids", f"veteran-friendly-audiologists-{st.lower().replace(' ', '-')}", f"Tips and directories for finding private audiologists in {st} who accept VA Community Care.", f"veteran audiologist {st}"))

ARTICLES = []
base_date = datetime.now() - timedelta(days=180)

def generate_article_body(title, category_key, keyword):
    cat_title = CATEGORIES[category_key]["title"]
    
    spin_intros = [
        f"<p>If you are a US military veteran searching for information on <strong>{keyword}</strong>, you are not alone. Thousands of veterans face questions about their auditory health and benefits every year. In this comprehensive guide, we will explore everything you need to know about {title.lower()} and how it impacts your daily life.</p><p>Hearing loss is the most common service-connected disability, meaning the VA is well-equipped to handle claims related to {keyword}. However, the process can still be daunting. We are here to simplify it for you.</p>",
        f"<p>Navigating the world of VA benefits and audiology can be overwhelming. When looking into <strong>{keyword}</strong>, it is crucial to understand all your options. This article serves as your ultimate resource for {title.lower()}, breaking down the complexities into actionable steps.</p><p>Veterans often wait years before seeking help for hearing issues. By taking the time to research {keyword}, you are taking a vital step toward improving your overall health and well-being.</p>",
        f"<p>Welcome to our deep dive into <strong>{keyword}</strong>. For veterans, understanding the intricacies of {title.lower()} can be the difference between getting fully funded top-tier hearing aids and paying out of pocket. Our goal is to equip you with the knowledge you need.</p><p>The Department of Veterans Affairs has established specific protocols regarding {keyword}. By familiarizing yourself with these rules, you can advocate for yourself more effectively during your audiology appointments.</p>"
    ]
    
    spin_details = [
        f"<h2>Why {cat_title} Matters for Veterans</h2><p>In the realm of {cat_title}, staying informed empowers you to advocate for yourself. The VA healthcare system is vast, and knowing the specific protocols for {keyword} can save you months of waiting. Whether you are dealing with noise-induced hearing loss from artillery fire or age-related decline, the principles of {cat_title} apply.</p><p>Many veterans are unaware that they might qualify for the Community Care network if wait times at their local VA clinic exceed 28 days. This is especially relevant when dealing with {keyword}. Always ask your primary care provider about alternative scheduling options if you are experiencing significant delays.</p>",
        f"<h2>The Impact of {keyword} on Daily Life</h2><p>Addressing {keyword} is not just about hearing better; it's about staying connected. Untreated hearing loss has been linked to cognitive decline, isolation, and depression in older adults. Within the context of {cat_title}, the VA provides extensive support networks, including support groups and specialized therapies.</p><p>When you begin the process of addressing {keyword}, you will likely undergo a comprehensive audiogram. This test determines your precise levels of hearing loss across different frequencies, allowing the audiologist to program your devices specifically to your needs.</p>"
    ]
    
    spin_actions = [
        f"<h2>Step-by-Step Guidance for {keyword}</h2><p>To effectively handle matters related to {keyword}, follow these steps:</p><ol><li><strong>Schedule an Evaluation:</strong> Contact your local VA medical center's audiology department or request a referral through your Primary Care Provider.</li><li><strong>Gather Documentation:</strong> Have your DD-214, service medical records, and any private audiograms ready. Proving service connection is crucial.</li><li><strong>Attend the Exam:</strong> Be honest about how your hearing impacts your quality of life. Don't downplay your symptoms.</li><li><strong>Follow Up:</strong> Don't hesitate to ask for adjustments or second opinions if your hearing aids are not functioning correctly.</li></ol>",
        f"<h2>Actionable Steps: Navigating {keyword}</h2><p>Taking action on {keyword} requires a structured approach. First, ensure you are enrolled in VA healthcare. If you aren't, you must apply via VA.gov or in person. Once enrolled, request an audiology consult. During your appointment regarding {keyword}, make sure to discuss all your symptoms, including tinnitus or vertigo.</p><p>Remember that you have the right to request specific styles of hearing aids (like receiver-in-canal or behind-the-ear), though the final decision rests on clinical necessity as determined by the VA audiologist.</p>"
    ]
    
    intro = random.choice(spin_intros)
    details = random.choice(spin_details)
    actions = random.choice(spin_actions)
    
    body = f"""
    <div class="introduction">
        {intro}
    </div>

    <div class="key-takeaways" style="background-color: #f8f9fa; border-left: 4px solid #0d47a1; padding: 15px; margin: 20px 0;">
        <h3>Key Takeaways</h3>
        <ul>
            <li>Understanding <strong>{keyword}</strong> is the first step toward better hearing health.</li>
            <li>The Department of Veterans Affairs offers various resources related to {cat_title}.</li>
            <li>Always consult with a licensed VA audiologist before making decisions about your hearing care.</li>
            <li>Keep a detailed log of your symptoms and how they affect your daily communication.</li>
        </ul>
    </div>

    <div class="ad-container" style="margin: 30px 0; text-align: center; background: #eee; padding: 20px;">
        <!-- AdSense Placeholder: Top Banner -->
        <p style="color: #888;">[AdSense Advertisement Space]</p>
    </div>

    {details}
    
    <div class="table-responsive" style="margin: 30px 0;">
        <table class="comparison-table" style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #0d47a1; color: white;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Factor</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Description</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Relevance to Veterans</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">Cost of Devices</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Often fully covered if enrolled in VA healthcare</td>
                    <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: green;">High</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">Technology Level</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Premium, state-of-the-art models (Bluetooth, rechargeable)</td>
                    <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: green;">High</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">Batteries & Supplies</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Free batteries and wax guards supplied via mail order</td>
                    <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: green;">High</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">Wait Times</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Varies heavily by regional VA medical center</td>
                    <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: orange;">Medium</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="ad-container" style="margin: 30px 0; text-align: center; background: #eee; padding: 20px;">
        <!-- AdSense Placeholder: Mid-Content -->
        <p style="color: #888;">[AdSense Advertisement Space]</p>
    </div>

    {actions}

    <h2>Frequently Asked Questions</h2>
    <div class="faq-section" style="margin-top: 20px;">
        <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
            <h4 style="margin-bottom: 5px; color: #0d47a1;">Is {keyword} covered by the VA?</h4>
            <p style="margin: 0;">Coverage depends on whether your condition is deemed service-connected or if you meet specific income thresholds (Group 8 exclusions). However, many veterans qualify for hearing care even without a service connection. Always check with your local VA eligibility office.</p>
        </div>
        <div class="faq-item" style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
            <h4 style="margin-bottom: 5px; color: #0d47a1;">How long does the process take?</h4>
            <p style="margin: 0;">From your initial appointment request to receiving your programmed hearing devices, the timeline can range from a few weeks to several months, heavily dependent on your local clinic's backlog.</p>
        </div>
        <div class="faq-item" style="margin-bottom: 20px; padding-bottom: 15px;">
            <h4 style="margin-bottom: 5px; color: #0d47a1;">Can I go to a civilian audiologist?</h4>
            <p style="margin: 0;">Yes, but only if the VA refers you out through the Community Care network. If you go to a civilian provider without prior authorization, the VA will not cover the cost of the devices or the exam.</p>
        </div>
    </div>
    """
    return body

for i, (title, category, slug, desc, keyword) in enumerate(raw_articles):
    publish_date = base_date + timedelta(days=i*5)
    ARTICLES.append({
        "title": title,
        "slug": slug,
        "category": category,
        "description": desc,
        "keyword": keyword,
        "publish_date": publish_date.strftime("%Y-%m-%d"),
        "body": generate_article_body(title, category, keyword)
    })

PAGES = {
    "about": {
        "title": "About Us",
        "description": "Learn about Dr. Sarah Mitchell and the Hearing Aids Veterans Guide mission.",
        "body": f"""
        <h2>Our Mission</h2>
        <p>At the Hearing Aids Veterans Guide, our mission is simple: to provide US military veterans with clear, accurate, and actionable information about hearing loss, hearing aids, and VA benefits.</p>
        <h2>About {{author_name}}</h2>
        <p>{{author_bio}}</p>
        <p>We are not directly affiliated with the Department of Veterans Affairs, but we strive to be the most trusted independent resource for veterans navigating their auditory healthcare.</p>
        """
    },
    "contact": {
        "title": "Contact Us",
        "description": "Get in touch with the Hearing Aids Veterans Guide team.",
        "body": f"""
        <p>If you have questions, suggestions, or need further guidance, please don't hesitate to reach out.</p>
        <p>Email us at: <strong>{SITE_CONFIG['contact_email']}</strong></p>
        <p><em>Note: We cannot provide individualized medical advice or check the status of your VA claims. Please contact your local VA medical center for specific medical or benefits inquiries.</em></p>
        """
    },
    "privacy-policy": {
        "title": "Privacy Policy",
        "description": "Privacy policy for the Hearing Aids Veterans Guide website.",
        "body": """
        <h2>Introduction</h2>
        <p>Your privacy is important to us. This privacy policy explains how we collect, use, and protect your personal information.</p>
        <h2>Google AdSense and Cookies</h2>
        <p>We use Google AdSense to display advertisements. Google uses cookies to serve ads based on a user's prior visits to this website or other websites. You may opt out of personalized advertising by visiting Google's Ads Settings.</p>
        <h2>Log Data</h2>
        <p>We collect standard log data, including IP addresses, browser types, and pages visited, to analyze traffic and improve our site via Google Analytics 4 (GA4).</p>
        """
    },
    "terms-of-service": {
        "title": "Terms of Service",
        "description": "Terms and conditions for using our website.",
        "body": """
        <h2>Acceptance of Terms</h2>
        <p>By accessing this website, you agree to be bound by these Terms of Service.</p>
        <h2>Intellectual Property</h2>
        <p>All content, including text, graphics, and logos, is the property of Hearing Aids Veterans Guide unless otherwise stated.</p>
        <h2>Limitation of Liability</h2>
        <p>We are not liable for any direct or indirect damages arising from the use of this website. Information is provided "as is" for educational purposes only.</p>
        """
    },
    "disclaimer": {
        "title": "Medical & Legal Disclaimer",
        "description": "Important disclaimer regarding the information provided on this site.",
        "body": """
        <h2>Not Medical Advice</h2>
        <p>The information on this website is for educational and informational purposes only and does not constitute professional medical advice, diagnosis, or treatment. Always seek the advice of your audiologist, physician, or other qualified health provider with any questions you may have regarding a medical condition.</p>
        <h2>Not Affiliated with the VA</h2>
        <p>This website is an independent resource and is NOT officially affiliated with, endorsed by, or operated by the United States Department of Veterans Affairs (VA) or any other government agency.</p>
        """
    }
}

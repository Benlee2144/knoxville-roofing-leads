"""One-off pages: calculator, how it works, legal, contact, 404, thank-you."""
import json

DEFAULT_COSTS = {
    'architectural_per_sqft': [4.5, 7.5],
    'asphalt_3tab_per_sqft': [3.5, 5.5],
    'metal_exposed_fastener_per_sqft': [5.5, 10.0],
    'metal_standing_seam_per_sqft': [9.0, 16.0],
}


def build(g):
    esc, icon, simple_page = g['esc'], g['icon'], g['simple_page']
    facts = g['FACTS']
    brand, site = g['BRAND'], g['SITE']
    costs = {k: (facts.get('site_costs') or {}).get(k) or v for k, v in DEFAULT_COSTS.items()}
    license_url = facts.get('license_lookup_url', 'https://verify.tn.gov/')

    # ------------------------------------------------------------------ calculator
    materials = [('architectural_per_sqft', 'Architectural shingles (most common)'),
                 ('asphalt_3tab_per_sqft', '3-tab asphalt shingles'),
                 ('metal_exposed_fastener_per_sqft', 'Metal, exposed fastener'),
                 ('metal_standing_seam_per_sqft', 'Metal, standing seam')]
    options = ''.join(f'<option value="{k}">{label}</option>' for k, label in materials)
    form = g['lead_form'](f'{brand} - Cost Calculator', 'Knoxville, TN', '37919', preselect='Roof replacement',
                          title='Turn your estimate into real quotes')
    calc_card = f'''            <div class="calc-card" id="calculator" data-prices='{json.dumps(costs)}'>
                <h2>Estimate your new roof</h2>
                <div class="form-group">
                    <label for="calc-sqft">Home size (heated square feet)</label>
                    <input type="number" id="calc-sqft" value="2000" min="400" max="12000" step="50" inputmode="numeric">
                </div>
                <div class="form-group">
                    <span class="group-label" id="calc-stories-label">Stories</span>
                    <div class="pill-group" role="radiogroup" aria-labelledby="calc-stories-label">
                        <label class="pill"><input type="radio" name="calc-stories" value="1" checked><span>1 story</span></label>
                        <label class="pill"><input type="radio" name="calc-stories" value="1.5"><span>1.5 stories</span></label>
                        <label class="pill"><input type="radio" name="calc-stories" value="2"><span>2+ stories</span></label>
                    </div>
                </div>
                <div class="form-group">
                    <span class="group-label" id="calc-pitch-label">Roof steepness</span>
                    <div class="pill-group" role="radiogroup" aria-labelledby="calc-pitch-label">
                        <label class="pill"><input type="radio" name="calc-pitch" value="low"><span>Low / walkable</span></label>
                        <label class="pill"><input type="radio" name="calc-pitch" value="medium" checked><span>Average</span></label>
                        <label class="pill"><input type="radio" name="calc-pitch" value="steep"><span>Steep</span></label>
                    </div>
                </div>
                <div class="form-group">
                    <label for="calc-material">Material</label>
                    <select id="calc-material">{options}</select>
                </div>
                <label class="checkbox-label calc-garage"><input type="checkbox" id="calc-garage"><span class="checkbox-text">Include an attached two-car garage</span></label>
                <div class="calc-result" aria-live="polite">
                    <span class="calc-result-label">Estimated installed cost</span>
                    <strong id="calc-range">&nbsp;</strong>
                    <span id="calc-detail" class="calc-result-detail">&nbsp;</span>
                </div>
                <a href="#quote" class="btn-primary btn-block">Get exact quotes {icon('arrow-right')}</a>
                <p class="calc-disclaimer">A planning estimate only, based on typical Knoxville-area prices. Real quotes depend on your roof's layout, layers, decking and access.</p>
            </div>'''
    calc_body = f'''    <section class="hero calc-hero">
        <div class="hero-overlay"></div>
        <div class="container hero-content">
            <div class="hero-text">
                <div class="hero-badge"><span class="badge-icon">{icon('calculator')}</span><span>Free tool for East Tennessee homeowners</span></div>
                <h1 class="hero-title">Roof Replacement <span class="highlight">Cost Calculator</span></h1>
                <p class="hero-subtitle">Get a ballpark price for a new roof in about 30 seconds, then compare real quotes from up to 3 licensed local roofers.</p>
                <div class="hero-features">
                    <div class="hero-feature"><span class="feature-check">{icon('check')}</span><span>Based on Knoxville-area price ranges</span></div>
                    <div class="hero-feature"><span class="feature-check">{icon('check')}</span><span>Shingles or metal</span></div>
                    <div class="hero-feature"><span class="feature-check">{icon('check')}</span><span>No email needed to see your estimate</span></div>
                </div>
            </div>
{calc_card}
        </div>
    </section>'''
    method = f'''    <section class="content-section">
        <div class="container content-layout">
            <div class="prose">
                <h2>How the estimate works</h2>
                <p>Roofers price by the "square", which is 100 square feet of roof surface. We estimate your roof surface from your home's footprint (heated square feet divided by the number of stories), add room for eaves and overhangs, and adjust for how steep the roof is. An attached garage adds its own roof area.</p>
                <p>We then multiply by a typical installed price range for the material you picked. Installed prices include tear-off of one layer, underlayment, flashing, ridge vents and cleanup in most quotes, but always check what each quote includes.</p>
                <h2>What pushes a quote up or down</h2>
                <ul>
                    <li><strong>Layers to remove.</strong> A second layer of old shingles means more labor and disposal.</li>
                    <li><strong>Rotten decking.</strong> Soft or damaged plywood is usually priced per sheet once the old roof is off.</li>
                    <li><strong>Roof shape.</strong> Valleys, dormers, skylights and chimneys add flashing work and waste.</li>
                    <li><strong>Steepness and height.</strong> Steep or tall roofs need extra safety gear and go slower.</li>
                    <li><strong>Material and warranty tier.</strong> Upgraded shingle lines and longer manufacturer warranties cost more.</li>
                    <li><strong>Insurance.</strong> If storm damage is covered, your out-of-pocket cost may be closer to your deductible.</li>
                </ul>
                <p>The only way to know your real price is to get written quotes. Comparing two or three of them also shows you quickly if one roofer is far out of line.</p>
            </div>
            <aside class="content-aside">
                <div class="aside-card">
                    <h3>Roof size cheat sheet</h3>
                    <ul class="check-list">
                        <li>{icon('check')}<span>1,500 sq ft ranch: about 18-20 squares</span></li>
                        <li>{icon('check')}<span>2,000 sq ft two-story: about 13-15 squares</span></li>
                        <li>{icon('check')}<span>2,500 sq ft ranch with garage: about 32-36 squares</span></li>
                    </ul>
                    <p class="aside-meta">Rough figures for an average-pitch roof.</p>
                </div>
                <div class="aside-card">
                    <h3>Related guides</h3>
                    <ul class="link-list">
                        <li><a href="/blog/roof-replacement-cost-knoxville/">Roof replacement cost in Knoxville</a></li>
                        <li><a href="/blog/best-roofing-materials-tennessee/">Best roofing materials for Tennessee</a></li>
                        <li><a href="/blog/metal-roof-pros-cons/">Metal roof pros and cons</a></li>
                    </ul>
                </div>
            </aside>
        </div>
    </section>
    <section class="form-section">
        <div class="container hero-content">
            <div class="form-section-text">
                <span class="section-badge">NEXT STEP</span>
                <h2 class="section-title left">Get exact prices for your roof</h2>
                <p class="section-lead">Your estimate is a starting point. Up to 3 licensed local roofers can measure your roof and give you written quotes to compare, at no cost.</p>
                <ul class="check-list">
                    <li>{icon('check')}<span>Free inspections and written estimates</span></li>
                    <li>{icon('check')}<span>Licensed &amp; insured contractors</span></li>
                    <li>{icon('check')}<span>No obligation to hire anyone</span></li>
                </ul>
            </div>
{form}
        </div>
    </section>'''
    faqs = [
        {'q': 'How accurate is the roof cost calculator?',
         'a': 'It gives a planning range, not a quote. Two homes with the same square footage can have very different roofs. Use the range to budget and to sanity-check the written quotes you get.'},
        {'q': 'What is a roofing square?',
         'a': 'A square is 100 square feet of roof surface. A typical Knoxville-area house has somewhere between 15 and 35 squares depending on its size, number of stories and pitch.'},
        {'q': 'Does homeowners insurance pay for a new roof?',
         'a': 'Insurance usually covers sudden damage such as hail, wind or a fallen tree, not old age or wear. If a storm damaged your roof, have it inspected and document everything before you file a claim.'},
    ]
    faq_html, faq_schema = g['faq_section'](faqs, 'Roof Cost Calculator Questions')
    crumb_html, crumb_schema = g['breadcrumbs']([('Home', '/'), ('Roof Cost Calculator', '/roof-cost-calculator/')])
    app_schema = {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': 'Roof Replacement Cost Calculator',
                  'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'Any', 'url': site + '/roof-cost-calculator/',
                  'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}}
    page = [
        g['head']('Roof Replacement Cost Calculator | Knoxville, TN Estimate',
                  'Estimate the cost of a new roof in Knoxville in 30 seconds. Enter your home size, stories, pitch and material, then compare real quotes from local roofers.',
                  '/roof-cost-calculator/', schema=[app_schema, faq_schema, crumb_schema]),
        '<body>', g['header'](), calc_body, crumb_html, method, faq_html, g['footer'](), g['floating_cta'](), g['scripts'](),
    ]
    g['write']('roof-cost-calculator/index.html', '\n'.join(page))

    # ------------------------------------------------------------------ quote comparison worksheet
    rows = [
        ('Company name and TN license number', 'Look it up at verify.tn.gov before you sign.'),
        ('Proof of liability insurance (and workers\' comp)', 'Sent directly from their insurance agent.'),
        ('Total price', 'The number on the contract, not a verbal estimate.'),
        ('Price per square', 'Total divided by roof size in squares (100 sq ft each). Makes quotes comparable.'),
        ('Roof size they measured', 'If sizes differ a lot between roofers, ask why.'),
        ('Tear-off included? How many layers?', 'Overlay vs. tear-off is not a fair comparison.'),
        ('Shingle brand and product line', 'Same brand can mean very different product tiers.'),
        ('Algae-resistant shingles?', 'Helpful in humid East Tennessee summers.'),
        ('Underlayment type', 'Synthetic underlayment is common today; ask what is included.'),
        ('Ice and water shield (valleys, penetrations)', 'Where it goes and how much.'),
        ('Decking: price per sheet if rot is found', 'Get the unit price in writing.'),
        ('Flashing: new or reused?', 'Chimney, wall and pipe flashing are common leak points.'),
        ('Ventilation changes (ridge vent, intake)', 'Poor ventilation shortens shingle life.'),
        ('Drip edge and gutter apron', 'Should be standard on a full replacement.'),
        ('Permit: needed? Who pulls it?', 'Rules differ between city and county.'),
        ('Workmanship warranty (years, in writing)', 'Separate from the manufacturer warranty.'),
        ('Manufacturer warranty tier', 'Enhanced warranties often need a certified installer.'),
        ('Deposit and payment schedule', 'Tennessee limits home improvement deposits to one-third.'),
        ('Start date and expected duration', 'Most homes take 1-3 days once work begins.'),
        ('Cleanup, magnetic nail sweep, dumpster', 'Who protects landscaping and hauls debris.'),
    ]
    trs = ''.join(f'<tr><th scope="row">{esc(item)}<span>{esc(tip)}</span></th><td></td><td></td><td></td></tr>' for item, tip in rows)
    worksheet = f'''    <section class="content-section">
        <div class="container">
            <div class="worksheet-actions no-print">
                <p>Print this page (or save it as a PDF) and fill in one column per roofer. Gaps and big differences between columns are exactly what to ask about.</p>
                <button type="button" class="btn-outline" onclick="window.print()">Print the worksheet</button>
            </div>
            <div class="table-wrap">
                <table class="data-table worksheet">
                    <thead><tr><th>What to compare</th><th>Quote 1</th><th>Quote 2</th><th>Quote 3</th></tr></thead>
                    <tbody>{trs}</tbody>
                </table>
            </div>
            <div class="prose worksheet-notes">
                <h2>Red flags when comparing quotes</h2>
                <ul>
                    <li>One quote is far lower than the others and leaves out tear-off, decking or flashing.</li>
                    <li>The roofer won't put the price, materials or warranty in writing.</li>
                    <li>A large deposit up front, or pressure to sign the same day.</li>
                    <li>An offer to "cover your deductible" by padding what they send your insurer.</li>
                    <li>No Tennessee license where one is required, or no proof of insurance.</li>
                </ul>
                <p>If you're filing an insurance claim, remember that Tennessee law lets you cancel a roofing contract within three business days after your insurer tells you in writing that the claim isn't covered. See our <a href="/roof-insurance-claims/">insurance claims page</a>.</p>
            </div>
        </div>
    </section>'''
    simple_page('/compare-roofing-quotes/', f'How to Compare Roofing Quotes | Free Printable Worksheet',
                'A free, printable worksheet for comparing up to 3 roofing quotes line by line: price per square, materials, tear-off, decking, warranties, permits and deposits.',
                'How to Compare Roofing Quotes', 'A free worksheet for lining up quotes side by side, so you compare the same work and spot what\'s missing.',
                worksheet)

    # ------------------------------------------------------------------ how it works
    how = f'''    <section class="content-section">
        <div class="container narrow prose">
            <h2>What {brand} is</h2>
            <p>{brand} is a free referral service for homeowners and property owners in Knoxville and the surrounding East Tennessee counties. We are not a roofing company and we don't send crews. We pass your request to up to 3 independent local roofing contractors who handle your type of project, so you can compare quotes without calling around.</p>
            <h2>How it works</h2>
            <ol>
                <li><strong>You tell us about the job.</strong> Pick the type of project, enter your ZIP code and how soon you need it, and leave your contact details.</li>
                <li><strong>We match you with up to 3 roofers.</strong> We look for contractors who work in your area and do your kind of work: storm damage, replacement, repair, metal or commercial.</li>
                <li><strong>They contact you to set up an estimate.</strong> Roofers usually reach out within 24-48 hours to schedule a free inspection.</li>
                <li><strong>You compare and decide.</strong> Hire whoever earns it, or no one. There is no obligation and no fee to you.</li>
            </ol>
            <h2>How we make money</h2>
            <p>Contractors pay us for the introductions. That is why the service is free for you. It also means we have a reason to send your request only to roofers who are a good fit, because a bad match is a waste for everyone.</p>
            <h2 id="verify">What we ask of the roofers we work with</h2>
            <p>We work with contractors who tell us they hold the Tennessee license their work requires and carry liability insurance. We still recommend that you check both yourself before you sign anything.</p>
            <p>In Tennessee, roofing jobs of $25,000 or more require a state contractor's license. In Knox County, home roofing jobs from $3,000 to $24,999 also require a state Home Improvement license; neighboring counties are not on that list, so ask your local codes office what applies there. Tennessee also limits home improvement deposits to one-third of the contract price.</p>
            <ul>
                <li>Look up the contractor's license on the State of Tennessee's verification site: <a href="{esc(license_url)}" rel="noopener" target="_blank">verify.tn.gov</a>.</li>
                <li>Ask for a certificate of insurance sent directly from their insurance agent.</li>
                <li>Get every price, material and warranty in writing.</li>
                <li>Never pay a large deposit to someone who just knocked on your door after a storm.</li>
            </ul>
            <h2>Talk to a person</h2>
            <p>Prefer the phone? Call or text {g['CONTACT_NAME']} at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>. Share your address and what's going on with your roof, and your request will be passed to local roofers who serve your area.</p>
            <h2>Your information</h2>
            <p>We share your request only with the contractors matched to your project. We don't sell your information to marketing lists. You can ask us to stop contacting you or delete your information at any time through our <a href="/contact/">contact page</a>. See our <a href="/privacy/">privacy policy</a> for details.</p>
        </div>
    </section>'''
    simple_page('/how-it-works/', f'How It Works | {brand}',
                'How our free roofing quote service works: tell us about your roof, get matched with up to 3 licensed local roofers, and compare quotes with no obligation.',
                'How It Works', 'A free, no-pressure way for East Tennessee homeowners to compare roofing quotes.', how)

    # ------------------------------------------------------------------ about
    about = f'''    <section class="content-section">
        <div class="container narrow prose">
            <h2>Who runs this site</h2>
            <p>{brand} is run by {g['CONTACT_NAME']}. If you have a question about your roof, your quote request or this site, you can call or text {g['CONTACT_NAME']} directly at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>.</p>
            <h2>Why it exists</h2>
            <p>Getting a fair price on a roof usually means calling around, waiting for callbacks and trying to compare quotes that don't line up. This site does the first part for you: tell us about your roof once, and up to 3 licensed, insured local roofers who handle your kind of work reach out with free estimates. You compare them and decide, or decide not to hire anyone.</p>
            <h2>What we are, and what we aren't</h2>
            <ul>
                <li>We are a free referral service for homeowners and property owners in Knoxville and the surrounding East Tennessee counties.</li>
                <li>We are not a roofing company. We don't send crews, sell materials or do the work.</li>
                <li>We don't sell your information to marketing lists. Your request goes only to the roofers matched to your project.</li>
            </ul>
            <h2>How we make money</h2>
            <p>Roofing contractors in our network pay us for introductions. That's why the service is free for homeowners. It also gives us every reason to send your request only to roofers who are a good fit.</p>
            <h2>How we keep our information honest</h2>
            <ul>
                <li>Prices, Tennessee laws and local facts in our guides come from published sources, and we link to them.</li>
                <li>We don't publish made-up reviews, ratings or savings claims.</li>
                <li>Listings on our <a href="/roofers/">East Tennessee Roofer Map</a> come from each company's own website, and companies can ask us to update or remove them.</li>
                <li>We review and update our guides when prices, laws or advice change.</li>
            </ul>
            <h2>Get in touch</h2>
            <p>Call or text <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>, use our <a href="/contact/">contact page</a>, or <a href="/#quote">request free roofing quotes</a>.</p>
        </div>
    </section>'''
    simple_page('/about/', f'About Us | {brand}',
                f'{brand} is a free roofing quote referral service for Knoxville and East Tennessee, run by {g["CONTACT_NAME"]}. How it works, how we make money and how we keep information honest.',
                f'About {brand}', 'A free, honest way for East Tennessee homeowners to compare roofing quotes.', about,
                schema=[{'@context': 'https://schema.org', '@type': 'AboutPage', 'name': f'About {brand}', 'url': site + '/about/'}])

    # ------------------------------------------------------------------ privacy
    privacy = f'''    <section class="content-section">
        <div class="container narrow prose legal">
            <p><em>Effective {g['TODAY']}</em></p>
            <h2>Who we are</h2>
            <p>{brand} ({site.replace('https://', '')}) is a free referral service that connects people who need roofing work with independent roofing contractors in East Tennessee. This policy explains what we collect, how we use it and the choices you have.</p>
            <h2>Information you give us</h2>
            <p>When you request quotes we collect the details you enter: the type of project, ZIP code, timeframe, whether you own the property, your name, phone number and email address, and your consent to be contacted. If you use the contact form we collect your name, email address and message.</p>
            <h2>Information collected automatically</h2>
            <p>We use Google Analytics to understand how visitors use the site (for example, pages viewed, device type and approximate location). Google Analytics uses cookies. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener" target="_blank">Google Analytics opt-out browser add-on</a>.</p>
            <h2>Advertising</h2>
            <p>Some pages show ads served by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads based on your visits to this site and other sites on the internet. You can opt out of personalized advertising by visiting <a href="https://adssettings.google.com" rel="noopener" target="_blank">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">www.aboutads.info</a>.</p>
            <h2>How we use your information</h2>
            <ul>
                <li>To match your request with up to 3 roofing contractors who serve your area and pass your details to them so they can contact you about your project.</li>
                <li>To reply to messages you send us.</li>
                <li>To keep the site working, prevent spam and improve our service.</li>
            </ul>
            <h2>Who we share it with</h2>
            <p>We share quote requests only with the contractors matched to your project, and with service providers that help us run the site (for example, Formspree, which processes our forms, and Google, for analytics and ads). We do not sell your personal information to marketing lists. We may disclose information if required by law.</p>
            <h2>Calls and texts</h2>
            <p>If you consent, contractors may contact you by phone, text or email about your project. Message and data rates may apply. You can reply STOP to any text to opt out, or tell the contractor you no longer wish to be contacted.</p>
            <h2>Your choices</h2>
            <p>You can ask us to access, correct or delete the information you submitted, or to stop sharing it, by writing to us through our <a href="/contact/">contact page</a>. Contractors who already received your request keep their own records under their own policies.</p>
            <h2>Data retention and security</h2>
            <p>We keep quote requests only as long as needed to provide the service and for our records, and we use reasonable safeguards. No method of transmission over the internet is completely secure.</p>
            <h2>Children</h2>
            <p>This site is meant for adults arranging work on property. We do not knowingly collect information from children under 13.</p>
            <h2>Changes</h2>
            <p>We may update this policy. The effective date at the top shows when it last changed.</p>
            <h2>Contact</h2>
            <p>Questions about this policy? Call or text {g['CONTACT_NAME']} at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>, or reach us through our <a href="/contact/">contact page</a>.</p>
        </div>
    </section>'''
    simple_page('/privacy/', f'Privacy Policy | {brand}', f'How {brand} collects, uses and shares information, including cookies, Google Analytics, Google AdSense and quote requests.',
                'Privacy Policy', None, privacy, cta=False)

    # ------------------------------------------------------------------ terms
    terms = f'''    <section class="content-section">
        <div class="container narrow prose legal">
            <p><em>Effective {g['TODAY']}</em></p>
            <h2>Our service</h2>
            <p>{brand} is a free referral service. We are not a roofing contractor, we do not perform roofing work, and we do not employ the contractors we refer. Contractors in our network are independent businesses responsible for their own work, pricing, licensing, insurance and warranties.</p>
            <h2>No guarantees</h2>
            <p>We try to refer contractors who are a good fit for your project, but we do not guarantee that a contractor will contact you, provide a quote, or perform work to any standard. Any agreement you make is between you and the contractor. Please verify licenses and insurance and get all terms in writing before hiring.</p>
            <h2>Cost information</h2>
            <p>Prices, ranges and calculator results on this site are general estimates for planning. They are not quotes or offers and may not reflect the price of your project.</p>
            <h2 id="consent">Consent to be contacted</h2>
            <p>By submitting a quote request and checking the consent box, you agree that {brand} and up to 3 roofing contractors in our network may contact you about your project at the phone number and email address you provided, including by calls and text messages that may be sent using automated technology. Consent is not a condition of any purchase. Message and data rates may apply. Message frequency varies. You can opt out at any time by replying STOP to a text message, telling the caller, or contacting us through our <a href="/contact/">contact page</a>.</p>
            <h2>Acceptable use</h2>
            <p>Please submit only accurate information about property you own, manage or are authorized to arrange work on. Do not submit requests on behalf of others without permission.</p>
            <h2>Limitation of liability</h2>
            <p>To the fullest extent permitted by law, {brand} is not liable for any damages arising from your use of this site or from work performed, or not performed, by any contractor. The site is provided "as is".</p>
            <h2>Governing law</h2>
            <p>These terms are governed by the laws of the State of Tennessee.</p>
            <h2>Contact</h2>
            <p>Questions? Call or text {g['CONTACT_NAME']} at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>, or reach us through our <a href="/contact/">contact page</a>.</p>
        </div>
    </section>'''
    simple_page('/terms/', f'Terms of Use & Consent | {brand}', f'Terms of use for {brand}, including our consent to be contacted by roofing contractors and our role as a free referral service.',
                'Terms of Use & Consent', None, terms, cta=False)

    # ------------------------------------------------------------------ contact
    contact = f'''    <section class="content-section">
        <div class="container narrow">
            <div class="contact-layout">
                <form class="contact-form" action="{g['FORMSPREE']}" method="POST">
                    <div class="form-group"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
                    <div class="form-group"><label for="c-email">Email</label><input id="c-email" type="email" name="email" autocomplete="email" required></div>
                    <div class="form-group"><label for="c-message">Message</label><textarea id="c-message" name="message" rows="6" required></textarea></div>
                    <input type="hidden" name="_subject" value="Website contact message">
                    <input type="hidden" name="source" value="Contact page">
                    <input type="text" name="_gotcha" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true">
                    <button type="submit" class="submit-btn"><span class="btn-text">Send Message</span></button>
                </form>
                <div class="aside-card contact-card">
                    <h3>Call or text {g['CONTACT_NAME']}</h3>
                    <p>The quickest way to reach us.</p>
                    <a href="tel:{g['PHONE_TEL']}" class="contact-line">{icon('phone')}{g['PHONE_DISPLAY']}</a>
                    <a href="{g['SMS_HREF']}" class="contact-line">{icon('message')}Send a text</a>
                </div>
                <div class="aside-card">
                    <h3>Looking for roofing quotes?</h3>
                    <p>The fastest way to get help with your roof is our quote form. It goes straight to local roofers who serve your area.</p>
                    <a href="/#quote" class="btn-primary btn-block">Get Free Quotes</a>
                </div>
            </div>
        </div>
    </section>'''
    simple_page('/contact/', f'Contact Us | {brand}', f'Contact {brand} with questions about our free roofing quote service, your information, or partnering as a roofing contractor.',
                'Contact Us', f'Questions about the service, your information, or joining our contractor network? Call or text {g["CONTACT_NAME"]} at {g["PHONE_DISPLAY"]}, or send a note below.', contact, cta=False)

    # ------------------------------------------------------------------ 404
    links = ''.join(f'<a class="area-link" href="{h}">{t}</a>' for h, t in g['NAV'])
    nf = f'''    <section class="content-section">
        <div class="container narrow center">
            <p>The page you were looking for may have moved. These are the most popular places to go next:</p>
            <div class="area-link-grid center">{links}</div>
        </div>
    </section>'''
    simple_page('/404.html', f'Page Not Found | {brand}', 'This page could not be found.', 'Fumble! Page not found', None, nf, noindex=True)

    # ------------------------------------------------------------------ thank you
    ty = f'''    <main class="thank-you-section">
        <div class="container">
            <div class="thank-you-card">
                <div class="thank-you-icon"><svg class="icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg></div>
                <h1>Touchdown! You're all set</h1>
                <p class="thank-you-lead">We received your request. Keep your phone handy: local roofers usually reach out within 24-48 hours, often sooner for emergencies.</p>
                <p class="thank-you-contact">Haven't heard back in 48 hours, or have a question? Call or text {g['CONTACT_NAME']} at <a href="tel:{g['PHONE_TEL']}">{g['PHONE_DISPLAY']}</a>.</p>
                <ol class="next-steps">
                    <li><span class="next-step-icon">{icon('phone-call')}</span><div><strong>Answer unknown 865 numbers</strong><p>Roofers may call or text from numbers you don't recognize. A quick call is the fastest way to book your free inspection.</p></div></li>
                    <li><span class="next-step-icon">{icon('clipboard-check')}</span><div><strong>Get written estimates</strong><p>Ask each roofer for an itemized quote covering materials, tear-off, and warranty so you can compare fairly.</p></div></li>
                    <li><span class="next-step-icon">{icon('scale')}</span><div><strong>Choose on your terms</strong><p>There's no obligation. Hire whoever earns it, or nobody at all.</p></div></li>
                </ol>
                <div class="aside-card prepare-card">
                    <h3>Have these ready for the roofer</h3>
                    <ul class="check-list">
                        <li>{icon('check')}<span>Photos of any damage, inside and out</span></li>
                        <li>{icon('check')}<span>Roughly how old the roof is</span></li>
                        <li>{icon('check')}<span>Your insurance policy and claim number, if you filed one</span></li>
                        <li>{icon('check')}<span>A list of questions (see our guide below)</span></li>
                    </ul>
                </div>
                <div class="button-row center-row">
                    <a href="/compare-roofing-quotes/" class="btn-primary">Get the Quote Comparison Worksheet</a>
                    <a href="/blog/questions-to-ask-roofing-contractor/" class="btn-outline">Questions to Ask</a>
                </div>
            </div>
        </div>
    </main>'''
    page = [g['head'](f'Request Received | {brand}', 'Your roofing quote request was received.', '/thank-you/', noindex=True),
            '<body class="thank-you-page">', g['header']('/#quote'), ty, g['footer'](), g['scripts']()]
    g['write']('thank-you/index.html', '\n'.join(page))

import os
import glob

files = glob.glob(r'c:\Users\admin\Desktop\iptv-website\*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Title replacements
    content = content.replace('| MyIPTV Blog</title>', '| OttOcean IPTV Blog</title>')
    content = content.replace('<title>Blog — MyIPTV Premium Service</title>', '<title>Blog — OttOcean IPTV</title>')
    content = content.replace('<title>Contact Us — MyIPTV Premium Service</title>', '<title>Contact Us — OttOcean IPTV</title>')
    content = content.replace('<title>FAQ — MyIPTV Premium Service</title>', '<title>FAQ — OttOcean IPTV</title>')
    content = content.replace('<title>Pricing Plans — MyIPTV Premium Service</title>', '<title>Pricing Plans — OttOcean IPTV</title>')
    
    # 2. General branding replacements
    # Nav logo
    content = content.replace('<a href="index.html" class="logo" id="nav-logo">MyIPTV</a>', '<a href="index.html" class="logo" id="nav-logo">OttOcean IPTV</a>')
    # Footer logo
    content = content.replace('<a href="index.html" class="footer-logo">MyIPTV</a>', '<a href="index.html" class="footer-logo">OttOcean IPTV</a>')
    content = content.replace('<a href="index.html" class="footer-logo" id="footer-logo">MyIPTV</a>', '<a href="index.html" class="footer-logo" id="footer-logo">OttOcean IPTV</a>')
    
    # Footer copyright
    content = content.replace('MyIPTV. All rights reserved.</p>', 'OttOcean IPTV. All rights reserved.</p>')
    
    # Contact emails
    content = content.replace('support@myiptv.com', 'support@ottocean.com')
    
    # Pricing
    content = content.replace('3 Months — €29', '3 Months — €39')
    content = content.replace('6 Months — €39', '6 Months — €49')
    content = content.replace('12 Months — €59', '12 Months — €65')
    content = content.replace('OttOcean 3 Months — €29', 'OttOcean 3 Months — €39')
    content = content.replace('OttOcean 6 Months — €39', 'OttOcean 6 Months — €49')
    content = content.replace('OttOcean 12 Months — €59', 'OttOcean 12 Months — €65')
    
    # Blog.html heading and descriptions
    content = content.replace('<h1>The MyIPTV<br><span>Blog</span></h1>', '<h1>The OttOcean IPTV<br><span>Blog</span></h1>')
    content = content.replace('content="IPTV tips, guides, and news from the MyIPTV team.', 'content="IPTV tips, guides, and news from the OttOcean IPTV team.')
    content = content.replace('content="Everything you need to know before getting started with MyIPTV.', 'content="Everything you need to know before getting started with OttOcean IPTV.')
    content = content.replace('Everything you need to know before getting started with MyIPTV.', 'Everything you need to know before getting started with OttOcean IPTV.')
    content = content.replace('content="Get in touch with MyIPTV support.', 'content="Get in touch with OttOcean IPTV support.')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

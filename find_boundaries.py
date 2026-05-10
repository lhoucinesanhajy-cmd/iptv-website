import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

hero_end = 0
pricing_start = 0
pricing_end = 0
features_start = 0

for i, line in enumerate(lines):
    if '<section id="hero">' in line:
        pass
    if '<section id="pricing">' in line:
        pricing_start = i
    if '<section id="features">' in line:
        features_start = i

# Find the end of pricing section
for i in range(features_start - 1, pricing_start, -1):
    if '</section>' in lines[i]:
        pricing_end = i
        break

# Find the end of hero section
categories_start = 0
for i, line in enumerate(lines):
    if '<section id="categories">' in line:
        categories_start = i
        break

for i in range(categories_start - 1, -1, -1):
    if '</section>' in lines[i]:
        hero_end = i
        break

print(f"Hero ends at line {hero_end + 1}")
print(f"Pricing starts at line {pricing_start + 1}")
print(f"Pricing ends at line {pricing_end + 1}")
print(f"Categories starts at line {categories_start + 1}")


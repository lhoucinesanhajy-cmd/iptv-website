// Node.js script to generate favicon.png using pure SVG -> PNG approach
// This creates an SVG-based favicon matching the OttOcean brand:
// circular icon with orange/green/red swirl and a black play button center

const fs = require('fs');
const path = require('path');

// Generate SVG content for the favicon
const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <!-- Circular clip -->
    <clipPath id="circle-clip">
      <circle cx="256" cy="256" r="248"/>
    </clipPath>
    <!-- Orange arc gradient -->
    <radialGradient id="gradOrange" cx="30%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FF9500"/>
      <stop offset="100%" stop-color="#FF6B00"/>
    </radialGradient>
    <!-- Green arc gradient -->
    <radialGradient id="gradGreen" cx="70%" cy="70%" r="60%">
      <stop offset="0%" stop-color="#34C759"/>
      <stop offset="100%" stop-color="#27A045"/>
    </radialGradient>
    <!-- Red arc gradient -->
    <radialGradient id="gradRed" cx="50%" cy="20%" r="70%">
      <stop offset="0%" stop-color="#FF3B30"/>
      <stop offset="100%" stop-color="#D62020"/>
    </radialGradient>
    <!-- Drop shadow for play button -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(0,0,0,0.4)"/>
    </filter>
  </defs>

  <!-- White circular background -->
  <circle cx="256" cy="256" r="256" fill="#FFFFFF"/>

  <!-- === SWIRL SEGMENTS === -->
  <!-- Each segment is a thick arc created using path arcs -->

  <!-- Orange segment: top-left to bottom, spanning ~160 degrees -->
  <path d="M 256 256
    L 60 150
    A 210 210 0 0 1 256 46
    Z" fill="url(#gradOrange)" clip-path="url(#circle-clip)"/>

  <path d="M 256 256
    L 256 46
    A 210 210 0 0 1 462 200
    Z" fill="url(#gradGreen)" clip-path="url(#circle-clip)"/>

  <path d="M 256 256
    L 462 200
    A 210 210 0 0 1 120 440
    Z" fill="url(#gradRed)" clip-path="url(#circle-clip)"/>

  <path d="M 256 256
    L 120 440
    A 210 210 0 0 1 60 150
    Z" fill="url(#gradOrange)" clip-path="url(#circle-clip)" opacity="0.85"/>

  <!-- White inner circle to create donut ring effect -->
  <circle cx="256" cy="256" r="130" fill="#FFFFFF"/>

  <!-- Black play button triangle -->
  <polygon points="220,195 220,317 340,256" fill="#1A1A1A" filter="url(#shadow)"/>

  <!-- Outer border ring -->
  <circle cx="256" cy="256" r="248" fill="none" stroke="rgba(0,0,0,0.08)" stroke-width="4"/>
</svg>`;

// Write SVG file
const svgPath = path.join(__dirname, 'favicon.svg');
fs.writeFileSync(svgPath, svgContent, 'utf8');
console.log('favicon.svg created successfully!');
console.log('Path:', svgPath);

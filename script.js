/* Force HTTPS and WWW */
if (window.location.hostname.includes('ottocean.sbs')) {
    if (window.location.hostname !== 'www.ottocean.sbs' || window.location.protocol !== 'https:') {
        window.location.replace('https://www.ottocean.sbs' + window.location.pathname + window.location.search);
    }
}

/* ===================================================
   Navbar � scroll-driven background + mobile toggle
   Works across all pages (multi-page architecture)
   =================================================== */

const header    = document.getElementById('site-header');
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('nav-links');

/* 1. Transparent ? dark background on scroll */
function onScroll() {
    if (window.scrollY > 20) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* 2. Hamburger toggle */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        const isOpen = navLinks.classList.toggle('open');
        navToggle.classList.toggle('open', isOpen);
        navToggle.setAttribute('aria-expanded', String(isOpen));
    });
}

/* 3. Close drawer when a link is clicked (mobile) */
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks) navLinks.classList.remove('open');
        if (navToggle) {
            navToggle.classList.remove('open');
            navToggle.setAttribute('aria-expanded', 'false');
        }
    });
});

/* 4. Mark active page link based on current filename */
(function markActivePage() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (
            href === page ||
            (page === '' && href === 'index.html') ||
            (page === 'index.html' && href === 'index.html')
        ) {
            link.classList.add('active');
        }
    });
})();

/* 5. Footer year */
const yearEl = document.getElementById('footer-year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* ===================================================
   INFINITE MARQUEE GENERATOR � RELIABLE DIRECT URLS
   =================================================== */
function initMarquee() {
    const track = document.getElementById('marqueeTrack');
    if (!track) return;

    // Brands with reliable direct image URLs (Wikipedia SVGs + official CDNs)
    const brands = [
        {
            name: 'Netflix',
            img: 'https://upload.wikimedia.org/wikipedia/commons/7/7a/Logonetflix.png'
        },
        {
            name: 'Disney+',
            img: 'https://upload.wikimedia.org/wikipedia/commons/3/3e/Disney%2B_logo.svg'
        },
        {
            name: 'Prime Video',
            img: 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Prime_Video.png'
        },
        {
            name: 'Apple TV+',
            img: 'https://upload.wikimedia.org/wikipedia/commons/2/28/Apple_TV_Plus_Logo.svg'
        },
        {
            name: 'HBO',
            img: 'https://upload.wikimedia.org/wikipedia/commons/d/de/HBO_logo.svg'
        },
        {
            name: 'Hulu',
            img: 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Hulu_Logo.svg'
        },
        {
            name: 'ESPN',
            img: 'https://upload.wikimedia.org/wikipedia/commons/2/2f/ESPN_wordmark.svg'
        },
        {
            name: 'beIN Sports',
            img: 'https://upload.wikimedia.org/wikipedia/commons/4/4a/BeIN_Sports_logo.svg'
        },
        {
            name: 'Sky',
            img: 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Sky_Group_logo_2020.svg'
        },
        {
            name: 'Canal+',
            img: 'https://upload.wikimedia.org/wikipedia/commons/1/1a/Canal%2B.svg'
        },
        {
            name: 'BT Sport',
            img: 'https://upload.wikimedia.org/wikipedia/en/5/50/BT_Sport_logo.svg'
        },
        {
            name: 'FOX',
            img: 'https://upload.wikimedia.org/wikipedia/commons/3/thirty/Fox_Broadcasting_Company_logo.svg'
        },
        {
            name: 'NBC',
            img: 'https://upload.wikimedia.org/wikipedia/commons/3/3f/NBC_logo.svg'
        },
        {
            name: 'ABC',
            img: 'https://upload.wikimedia.org/wikipedia/commons/a/a4/ABC_logo_2021.svg'
        },
        {
            name: 'CBS',
            img: 'https://upload.wikimedia.org/wikipedia/commons/4/4e/CBS_logo.svg'
        },
        {
            name: 'UFC',
            img: 'https://upload.wikimedia.org/wikipedia/commons/9/92/UFC_Logo.svg'
        },
        {
            name: 'LaLiga',
            img: 'https://upload.wikimedia.org/wikipedia/commons/1/13/LaLiga.svg'
        },
        {
            name: 'Eurosport',
            img: 'https://upload.wikimedia.org/wikipedia/commons/7/76/Eurosport_Logo_2015.svg'
        },
        {
            name: 'DAZN',
            img: 'https://upload.wikimedia.org/wikipedia/commons/a/a2/DAZN_brand_logo.svg'
        },
        {
            name: 'Discovery+',
            img: 'https://upload.wikimedia.org/wikipedia/commons/5/52/Discovery%2B_logo.svg'
        },
        {
            name: 'Peacock',
            img: 'https://upload.wikimedia.org/wikipedia/commons/d/d3/NBCUniversal_Peacock_Logo.svg'
        },
        {
            name: 'Paramount+',
            img: 'https://upload.wikimedia.org/wikipedia/commons/a/a5/Paramount_Plus_logo.svg'
        },
        {
            name: 'Showtime',
            img: 'https://upload.wikimedia.org/wikipedia/commons/2/22/Showtime.svg'
        },
        {
            name: 'AMC',
            img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/thirty/AMC_Networks_logo.svg/1200px-AMC_Networks_logo.svg.png'
        },
        {
            name: 'FX',
            img: 'https://upload.wikimedia.org/wikipedia/commons/4/41/FX_International_logo.svg'
        },
        {
            name: 'Nat Geo',
            img: 'https://upload.wikimedia.org/wikipedia/commons/f/fc/Natgeologo.svg'
        },
        {
            name: 'BBC',
            img: 'https://upload.wikimedia.org/wikipedia/commons/e/eb/BBC_logo.svg'
        },
        {
            name: 'ITV',
            img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/ITV_logo_2013.svg/1200px-ITV_logo_2013.svg.png'
        },
        {
            name: 'YouTube',
            img: 'https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg'
        },
        {
            name: 'Twitch',
            img: 'https://upload.wikimedia.org/wikipedia/commons/2/26/Twitch_logo.svg'
        },
        {
            name: 'NBA',
            img: 'https://upload.wikimedia.org/wikipedia/en/0/03/National_Basketball_Association_logo.svg'
        },
        {
            name: 'NFL',
            img: 'https://upload.wikimedia.org/wikipedia/en/a/a2/National_Football_League_logo.svg'
        },
        {
            name: 'F1',
            img: 'https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg'
        },
        {
            name: 'MotoGP',
            img: 'https://upload.wikimedia.org/wikipedia/commons/4/forty/MotoGP_logo.svg'
        },
        {
            name: 'WWE',
            img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/WWE_Logo.svg/1200px-WWE_Logo.svg.png'
        },
        {
            name: 'Starz',
            img: 'https://upload.wikimedia.org/wikipedia/commons/8/85/Starz_2016.svg'
        }
    ];

    // Duplicate list for seamless infinite loop (CSS translates -50%)
    const allBrands = [...brands, ...brands];

    allBrands.forEach(({ name, img }) => {
        const card = document.createElement('div');
        card.className = 'logo-card';

        const image = document.createElement('img');
        image.src = img;
        image.alt = `${name} Logo`;
        image.loading = 'lazy';

        // Hide the whole card if the image fails to load
        image.onerror = () => { card.style.display = 'none'; };

        const label = document.createElement('span');
        label.className = 'logo-card-label';
        label.textContent = name;

        card.appendChild(image);
        card.appendChild(label);
        track.appendChild(card);
    });
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', initMarquee);


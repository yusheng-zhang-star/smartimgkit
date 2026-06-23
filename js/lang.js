/**
 * SmartImgKit - Language Switcher
 * Handles: Language switching, localStorage persistence, URL construction
 */

function getCurrentLanguage() {
  // Try localStorage first
  try {
    const saved = localStorage.getItem('lang_chosen');
    if (saved) return saved;
  } catch (e) {}
  
  // Fall back to URL path
  const path = window.location.pathname;
  if (path.startsWith('/es/') || path === '/es') return 'es';
  if (path.startsWith('/pt/') || path === '/pt') return 'pt';
  if (path.startsWith('/id/') || path === '/id') return 'id';
  
  // Default to English
  return 'en';
}

function getBasePath() {
  const path = window.location.pathname;
  // Remove language prefix if present
  if (path.startsWith('/es/')) return path.substring(3);
  if (path.startsWith('/pt/')) return path.substring(3);
  if (path.startsWith('/id/')) return path.substring(3);
  return path;
}

function constructLanguageURL(lang) {
  const basePath = getBasePath();
  if (lang === 'en') {
    return basePath;
  } else {
    // Ensure basePath starts with /
    const base = basePath.startsWith('/') ? basePath : '/' + basePath;
    return '/' + lang + base;
  }
}

function switchLanguage(lang) {
  // Save to localStorage
  try {
    localStorage.setItem('lang_chosen', lang);
  } catch (e) {}
  
  // Navigate to the new URL
  const newURL = constructLanguageURL(lang);
  window.location.href = newURL;
}

function updateLangUI() {
  const currentLang = getCurrentLanguage();
  
  // Update language dropdown button
  const langBtn = document.querySelector('.lang-btn');
  if (langBtn) {
    const flags = {
      'en': '🇬🇧',
      'es': '🇪🇸',
      'pt': '🇧🇷',
      'id': '🇮🇩'
    };
    const names = {
      'en': 'EN',
      'es': 'ES',
      'pt': 'PT',
      'id': 'ID'
    };
    
    // Check if the button has lang-flag and lang-name spans
    const flagSpan = langBtn.querySelector('.lang-flag');
    const nameSpan = langBtn.querySelector('.lang-name');
    
    if (flagSpan && nameSpan) {
      // Update existing spans
      flagSpan.textContent = flags[currentLang];
      nameSpan.textContent = names[currentLang];
    } else {
      // Update button text directly
      langBtn.innerHTML = flags[currentLang] + ' ' + names[currentLang];
    }
  }
  
  // Update language dropdown links
  const langDropdown = document.querySelector('.lang-dropdown');
  if (langDropdown) {
    const links = langDropdown.querySelectorAll('a');
    links.forEach(link => {
      const lang = link.getAttribute('hreflang');
      if (lang) {
        // Update href to point to the correct language version of the current page
        link.href = constructLanguageURL(lang);
        
        // Add onclick handler to save language preference and navigate
        link.onclick = function(e) {
          e.preventDefault();
          switchLanguage(lang);
          return false;
        };
      }
    });
  }
}

function toggleLangDropdown() {
  const dropdown = document.querySelector('.lang-dropdown');
  if (dropdown) {
    dropdown.classList.toggle('active');
  }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
  const langSwitcher = document.getElementById('langSwitcher');
  if (langSwitcher && !langSwitcher.contains(e.target)) {
    const dropdown = langSwitcher.querySelector('.lang-dropdown');
    if (dropdown) {
      dropdown.classList.remove('active');
    }
  }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
  updateLangUI();
});

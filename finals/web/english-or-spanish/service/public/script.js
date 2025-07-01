const ALLOWED_LANGUAGES = ['en', 'es'];
localStorage.language ??= getBrowserLanguage();

function getBrowserLanguage() {
    const [language] = (navigator.language || navigator.userLanguage).split('-');
    return ALLOWED_LANGUAGES.includes(language) ? language : 'en';
}

function applyLanguage() {
    const {language} = localStorage;
    const elements = document.querySelectorAll('[data-translation-key]');
    for (const element of elements) {
        const key = element.getAttribute('data-translation-key');
        fetch(`/translations/${language}/${key}`).then(async response => {
            // Might be inefficient, but it works...
            if (!response.ok)
                throw new Error(`Error fetching translation for ${key}`);

            const data = await response.json();
            element.textContent = data.toString();
        });
    }
}

applyLanguage();

document.getElementById('langToggle').addEventListener('click', () => {
    const next = localStorage.language === 'en' ? 'es' : 'en';
    localStorage.setItem('language', next);

    applyLanguage();
});

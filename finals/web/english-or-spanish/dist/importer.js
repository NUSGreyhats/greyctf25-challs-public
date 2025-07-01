const fs = require('fs');

function propertyAccessor(obj) {
    return new Proxy(obj, {
        get: (_, property) => {
            const props = property.split('.');

            let current = obj;
            for (const prop of props) current = current?.[prop];

            return current;
        }
    })
}

module.exports = {
    importLanguage: async (lang) => {
        const { default: language } = await import(`./languages/${lang}/lang.js`);
        return propertyAccessor(language);
    },
    importFile: new Proxy({}, {
        get: (_, file) => fs.readFileSync(file).toString(),
    }),
};

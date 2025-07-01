const express = require('express');
const importer = require('./importer');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));
app.get('/', (req, res) => res.sendFile(`${__dirname}/index.html`));

app.get('/translations/:lang/:prop', (req, res) => {
    const { lang, prop } = req.params;

    importer.importLanguage(lang)
        .then(language => {
            res.json(language[prop]);
        })
        .catch(err => {
            console.error(`Error fetching translation for ${lang}/${prop}:`, err.message);
            res.status(500).json({ error: err.message });
        });
});

app.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));

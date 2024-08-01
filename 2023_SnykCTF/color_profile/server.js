const fs = require('fs');
const ejs = require('ejs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.static(path.join(__dirname, 'public')));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

let profile = {
    color: "#FFFFFF"
};

app.post('/setColor', (req, res) => {
    const { color } = req.body;
    profile.color = color;
    res.json({ profileColor: color });
});

app.get('/', (req, res) => {
    fs.readFile(path.join(__dirname, 'views', 'index.ejs'), 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Internal Server Error');
        }
        
        const profilePage = data.replace(/<% profileColor %>/g, profile.color);
        const renderedHtml = ejs.render(profilePage, { profileColor: profile.color });
        res.send(renderedHtml);
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

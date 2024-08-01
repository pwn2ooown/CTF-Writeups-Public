const express = require('express');
const path = require('path');
const { Pandoc } = require('@hackmd/pandoc.js')
const crypto = require('crypto');
const fs = require('fs');

const app = express();
const port = 3001;

const outputFormats = {
    asciidoc: 'text/plain',
    markdown: 'text/plain',
    latex: 'application/x-latex'
};

async function actionPandoc(req, res) {
    const pandoc = new Pandoc();

    var path = '/tmp/' + Date.now();
    var content = req.body.comment;
    var title = crypto.randomBytes(20).toString('hex');
    const exportType = req.body.options;

    try {
        await pandoc.convertToFile(content, 'markdown', exportType, path, [
            '--metadata', `title=${title}`
        ]);

        var stream = fs.createReadStream(path);
        stream.on('error', function(err) {
            res.write('{"message": "error"}');
            res.end();

            return 0;
        });
        var filename = title;
        filename = encodeURIComponent(filename);

        res.setHeader('Content-disposition', `attachment; filename="${filename}.${exportType}"`);
        res.setHeader('Cache-Control', 'private');
        res.setHeader('Content-Type', `${outputFormats[exportType]}; charset=UTF-8`);
        res.setHeader('X-Robots-Tag', 'noindex, nofollow');

        stream.pipe(res);
    } catch (err) {
        res.json({
            message: err.message
        })
    }
}

app.use(express.urlencoded());

app.use(express.json());

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname + '/public', '/index.html'));
});

app.post('/api/generate', function (req, res) {
    actionPandoc(req, res);
});

app.listen(port);
console.log('Server started at http://localhost:' + port);
const https = require('https');
const fs = require('fs');

const categories = [
    { cat: 'Shampoo Automotivo', v: 'V-Floc', l: 'Lava Auto', d: 'Shampoo Neutro Dub', c: 'CC Shampoo' },
    { cat: 'Shampoo com Cera', v: 'V-Floc Wash & Wax', l: 'Lava Auto com Cera', d: 'Shampoo Wax Dub', c: 'CC Wash & Wax' },
    { cat: 'Desengraxante / APC', v: 'Sintra', l: 'APC Lincoln', d: 'All Cleaner Dub', c: 'CC APC' },
    { cat: 'Limpador de Rodas', v: 'Delet', l: 'Wheel Cleaner Lincoln', d: 'Wheel Cleaner Dub', c: 'CC Wheel' },
    { cat: 'Removedor de Ferro', v: 'Izer', l: 'Iron Remover Lincoln', d: 'Iron Remover Dub', c: 'CC Iron' },
    { cat: 'Cera Líquida', v: 'Blend Spray Wax', l: 'Cera Líquida Lincoln', d: 'Spray Wax Dub', c: 'CC Wax' },
    { cat: 'Selante', v: 'Native Brazilian Carnaúba', l: 'Selante Lincoln', d: 'Sealant Dub', c: 'CC Sealant' },
    { cat: 'Vitrificador', v: 'V-Plastic / V-Light', l: 'Vitrificador Lincoln', d: 'Coating Dub', c: 'CC Coating' },
    { cat: 'Condicionador de Plásticos', v: 'Revox', l: 'Restaurador Lincoln', d: 'Plastic Restorer Dub', c: 'CC Plastic' },
    { cat: 'Hidratante de Couro', v: 'Hidra Couro', l: 'Leather Care Lincoln', d: 'Leather Dub', c: 'CC Leather' },
    { cat: 'Limpa Vidros', v: 'Glass Cleaner', l: 'Limpa Vidros Lincoln', d: 'Glass Dub', c: 'CC Glass' },
    { cat: 'Removedor de Piche', v: 'Tar Remover', l: 'Removedor de Piche Lincoln', d: 'Tar Dub', c: 'CC Tar' }
];

function searchImage(query) {
    return new Promise((resolve) => {
        const req = https.get('https://html.duckduckgo.com/html/?q=' + encodeURIComponent(query + ' estetica automotiva'), (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                // DuckDuckGo lite img tags format
                const match = data.match(/<img[^>]+src=\"(\/\/external-content\.duckduckgo\.com\/iu\/\?u=[^\"]+)\"/i);
                if (match) {
                    resolve('https:' + match[1].replace(/&amp;/g, '&'));
                } else {
                    resolve('');
                }
            });
        });
        req.on('error', () => resolve(''));
    });
}

(async () => {
    const results = {};
    for (const row of categories) {
        results[row.cat] = { Vonixx: '', Lincoln: '', DubBoyz: '', CarCollection: '' };
        console.log('Searching for ' + row.cat + '...');
        results[row.cat].Vonixx = await searchImage('Vonixx ' + row.v);
        results[row.cat].Lincoln = await searchImage('Lincoln ' + row.l);
        results[row.cat].DubBoyz = await searchImage('Dub Boyz ' + row.d);
        results[row.cat].CarCollection = await searchImage('Car Collection Detailer ' + row.c);
        
        // Delay to avoid rate limiting
        await new Promise(r => setTimeout(r, 500));
    }
    fs.writeFileSync('images_db.json', JSON.stringify(results, null, 2));
    console.log('Done!');
})();

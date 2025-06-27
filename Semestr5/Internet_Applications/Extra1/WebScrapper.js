const https = require('https');
const cheerio = require('cheerio');

const baseURL = 'https://www.lego.com/en-pl/categories/all-sets';
const baseURL2 = 'https://www.lego.com/pl-pl/themes/speed-champions';
// const baseURL3 = 'https://www.lego.com/en-us/themes/technic';
const baseURL3 = 'https://www.lego.com/en-pl/themes/star-wars';
let currentPage = 1;
let properPage = true;
const data = []

const extractData = (html) => {
    const $ = cheerio.load(html);
    const data = [];

    $('#product-listing-grid li[data-test=product-item]').each((index, element) => {
        const row = $(element).find('.ProductLeaf_attributesRow__kjTcT');
        const priceRow = $(element).find('[data-test=product-leaf-price-row]');
        const nameRow = $(element).find('[data-test=product-leaf-title-row]')

        const nrOfBricks = $(row).find('[data-test=product-leaf-piece-count-label]').text();
        const rating = $(row).find('[data-test=product-leaf-rating-label]').text();
        const price = $(priceRow).find('[data-test=product-leaf-price]').text();
        const name = $(nameRow).find('[data-test=markup]').text();

        if (name.length > 0 && price.length > 0 && nrOfBricks.length > 0 && rating.length > 0){
            data.push([name, price, nrOfBricks, rating])
        }
    })

  return data;
};

const fetchPageData = (URL) => {
    return new Promise((resolve, reject) => {
        https.get(URL, (res) => {
            let html = '';

            res.on('data', (chunk) => {
                html += chunk;
            });

            res.on('end', () => {
                const newData = extractData(html);
                resolve(newData);
            });
        }).on('error', (err) => {
            reject(err);
        });
    });
};

const scrapeAllPages = async (baseURL) => {
    while (properPage) {
        let URL;
        if (currentPage === 1) {
            URL = baseURL;
        } else {
            URL = `${baseURL}?page=${currentPage}`;
        }

        try {
            console.log(`Fetching page ${currentPage}`);
            const pageData = await fetchPageData(URL);

            if (pageData.length > 0) {
                data.push(...pageData);
                currentPage += 1;
            } else {
                properPage = false;
                console.log('No more pages to scrape.');
            }
        } catch (error) {
            console.error('Error fetching URL:', error.message);
            properPage = false;
        }
    }

    console.log('Scraping complete.');
    return data;
};

const calculateUnitPrices = async (URL) => {
    let unitPrices = [];
    try{
        const scrapedData = await scrapeAllPages(URL);

        for (let i=0; i < scrapedData.length; i++){
            const name = scrapedData[i][0];
            const price = parseFloat(scrapedData[i][1].replace(',', '.'));
            const numberOfBricks = parseInt(scrapedData[i][2]);
            const rating = parseFloat(scrapedData[i][3]);
            const complexRatio = parseFloat(((price/(numberOfBricks*rating)).toFixed(2)));
            const simpleRatio = parseFloat((price/numberOfBricks).toFixed(2));
            unitPrices.push({Name: name, Price: price + " zł", NumberOfBricks: numberOfBricks, 
                Rating: rating, Ratio1: complexRatio, Ratio2: simpleRatio})
        }
    } catch (error){
        console.error(error.message)
    }
    unitPrices.sort((a, b) => a.Ratio2 - b.Ratio2);
    console.log(unitPrices.slice(0, 10));
    return unitPrices.slice(0, 10);
}

calculateUnitPrices(baseURL3);
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const QRCode = require("qrcode");
const Jimp = require("jimp");

const alphanumerics = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

// Format numbers with commas
const comma = (number) => {
    return number.toLocaleString("en-US");
};

// Hash QR Code data
const hashQRCodeData = (receiptData) => {
    let stringHolder = "";
    for (const key in receiptData) {
        stringHolder += receiptData[key];
    }
    return crypto.createHash("sha256").update(stringHolder).digest("hex");
};

// Chunk text into lines with a character limit
const saleReceiptChunker = (lineCharacterMax, stringText) => {
    const wordSet = stringText.split(" ");
    let printCharacterCount = 0;
    let printDigest = "";
    let currentLineCharMax = lineCharacterMax;

    wordSet.forEach((word) => {
        if (printCharacterCount + word.length <= currentLineCharMax) {
            printDigest += `${word} `;
            printCharacterCount += word.length + 1;
        } else {
            printDigest += `\n${word} `;
            printCharacterCount = word.length + 1;
        }
    });

    return printDigest.trim();
};

// Generate a QR Code image
const generateQRCodeImage = async (data) => {
    try {
        const dataHash = hashQRCodeData(data);
        const qrCodePath = path.resolve(__dirname, `./out_store/qr_${Date.now()}.png`);
        await QRCode.toFile(qrCodePath, dataHash, {
            width: 300,
            margin: 2,
        });
        return { path: qrCodePath, hash: dataHash };
    } catch (err) {
        console.error("Error generating QR Code:", err);
        throw err;
    }
};

// Generate transaction card with QR code
const generateTransactionCard = async (qrCodePath, data) => {
    try {
        const stagingPath = path.resolve(__dirname, "./static/out_store/");
        const templatePath = path.resolve(__dirname, data.print_data.item_media_plate_url);
        const outputFileName = `card_${Date.now()}.jpg`;
        const outputPath = path.join(stagingPath, outputFileName);

        const templateImage = await Jimp.read(templatePath);
        const qrCodeImage = await Jimp.read(qrCodePath);

        qrCodeImage.resize(300, 300);
        templateImage.composite(qrCodeImage, 660, 700); // Adjust positions as needed

        const font = await Jimp.loadFont(Jimp.FONT_SANS_32_BLACK);
        templateImage.print(font, 200, 200, data.print_data.heading);
        templateImage.print(font, 200, 600, data.print_data.sub_heading);
        templateImage.print(font, 200, 1000, new Date().toLocaleDateString());

        await templateImage.writeAsync(outputPath);

        return { status: true, url: outputPath };
    } catch (err) {
        console.error("Error generating transaction card:", err);
        return { status: false, message: `Unable to generate card: ${err.message}`, url: "" };
    }
};

// Generate receipt
const generateReceipt = async (qrCodePath, data) => {
    try {
        const stagingPath = path.resolve(__dirname, "./static/out_store/");
        const templatePath = path.resolve(__dirname, data.print_data.item_media_plate_url);
        const outputFileName = `receipt_${Date.now()}.jpg`;
        const outputPath = path.join(stagingPath, outputFileName);

        const templateImage = await Jimp.read(templatePath);
        const qrCodeImage = await Jimp.read(qrCodePath);

        qrCodeImage.resize(150, 150);
        templateImage.composite(qrCodeImage, 50, 50); // Adjust positions as needed

        const font = await Jimp.loadFont(Jimp.FONT_SANS_32_BLACK);
        templateImage.print(font, 200, 200, `Receipt ID: ${data.receipt_id}`);
        templateImage.print(font, 200, 300, `Date: ${new Date().toLocaleDateString()}`);
        templateImage.print(font, 200, 400, `Amount: $${comma(data.amount)}`);

        await templateImage.writeAsync(outputPath);

        return { status: true, url: outputPath };
    } catch (err) {
        console.error("Error generating receipt:", err);
        return { status: false, message: `Unable to generate receipt: ${err.message}`, url: "" };
    }
};

// Generate random alphanumeric string
const generateRandomString = (length) => {
    let result = "";
    for (let i = 0; i < length; i++) {
        result += alphanumerics.charAt(Math.floor(Math.random() * alphanumerics.length));
    }
    return result;
};

module.exports = {
    comma,
    hashQRCodeData,
    saleReceiptChunker,
    generateQRCodeImage,
    generateTransactionCard,
    generateReceipt,
    generateRandomString,
};

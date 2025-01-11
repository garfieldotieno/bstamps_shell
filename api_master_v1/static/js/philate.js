import { createHash } from 'crypto-js';
import { QRCode } from 'qrcode-generator';
import { Jimp } from 'jimp-browser';
import { fs } from 'browser-fs';

const alphanumerics = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

// Format numbers with commas
const comma = (number) => {
  return number.toLocaleString("en-US");
};

// Generate a random string
const generateRandomString = (length) => {
    let result = '';
    for (let i = 0; i < length; i++) {
      result += alphanumerics.charAt(Math.floor(Math.random() * alphanumerics.length));
    }
    return result;
  };


// Generate a hash
const generateDictHash = (data) => {
    const hash = createHash('sha256');
    let string_holder = "";
    data.keys().forEach((key) => {
        string_holder += data.get(key);
    });
    hash.update(string_holder);
    return hash.digest();
};

// Hash QR code data
const hashQRCodeData = (data) => {
    return generateDictHash(data);
  };


// Generate a QR code
const generateQRCode = (data) => {
  const qrCode = new QRCode();
  hash_data = hashQRCodeData(data)
  qrCode.addData(hash_data);
  qrCode.make();
  return qrCode.createDataURL();
};


// Sale receipt chunker
const saleReceiptChunker = (line_character_max, string_text) => {
    // TO DO: implement chunking logic
    //  identify the number of words in the input_string with their start and stop position
    //  map splitting points in the input_string
    //  count the words in the word_set and each time evaluate if the current word is an add_to_sentence or start_new_line

    word_set = string_text.split(" ");
    print_character_count = 0;
    word_list = [];
    print_digest = ""

    return print_digest;
  };


// Load an image
const loadImage = (url) => {
  return Jimp.read(url);
};

// Save an image
const saveImage = (image) => {
  return fs.writeFile('image.png', image.getBufferAsync());
};




// Generate transaction card
const generateTransactionCard = (transactionData) => {
  // TO DO: implement transaction card generation logic
  return transactionData;
};

// Generate receipt
const generateReceipt = (receiptData) => {
  // TO DO: implement receipt generation logic
  return receiptData;
};

export {
  comma,
  generateQRCode,
  generateHash,
  loadImage,
  saveImage,
  generateRandomString,
  hashQRCodeData,
  saleReceiptChunker,
  generateTransactionCard,
  generateReceipt,
};
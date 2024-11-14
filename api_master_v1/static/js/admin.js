
let APP_NAVIGATION =[];
 
let APP_PARENT_ELEMENT = document.querySelector('.parent_display_container');

window.addEventListener('DOMContentLoaded', function() {  
    refreshDisplay(); 
});


function refreshDisplay(){
    render_ui();
}

function getScreenMode(){
    if (window.innerWidth > 777){
      return 'large';
    }
    else if (window.innerWidth <= 777){
      return 'small';
    }
}

// test function to print yup
function render_ui(){
    var startX = 0;
    window.scrollTo(startX, 0);
  
    if(getScreenMode() == 'small'){
  
      if(APP_NAVIGATION.length == 0){
        APP_NAVIGATION.push('Bot');
        console.log(`starting render_ui in small mode, APP_NAVIGATION IS ${APP_NAVIGATION}`);
        generate_small_screen_binding_stucture();
        generate_static_bot_small();
      }
      else if(APP_NAVIGATION.length > 0){
        console.log(`continuing render_ui in small mode, APP_NAVIGATION IS ${APP_NAVIGATION}`);
        if(APP_NAVIGATION[0] == 'Bot'){
          generate_small_screen_binding_stucture();
          generate_static_bot_small();
        }
        else if (APP_NAVIGATION[0] == 'Home'){
          generate_small_screen_binding_stucture();
          generate_items_of_sale_small();
        }
        else if (APP_NAVIGATION[0] == 'About'){
          generate_small_screen_binding_stucture();
          generate_about_info_small();
        }
        else if (APP_NAVIGATION[0] == 'PromptCheckin'){
          generate_small_screen_binding_stucture();
          generate_prompt_mode();
        }
      }
    }
    else if (getScreenMode() == 'large'){
      
      if(APP_NAVIGATION.length == 0){
        APP_NAVIGATION =[];
        APP_NAVIGATION.push('Bot','Home');
        console.log(`starting render_ui in big mode, APP_NAVIGATION IS ${APP_NAVIGATION}`);
        
        generate_big_screen_binding_structure();
        generate_static_bot_big();
        }
      else if(APP_NAVIGATION.length > 0){
        console.log(`continuing render_ui in big mode, APP_NAVIGATION IS ${APP_NAVIGATION}`);
        
        if(APP_NAVIGATION[0] == 'Bot'){
          generate_big_screen_binding_structure();
          generate_static_bot_big();
        }
        else if (APP_NAVIGATION[0] == 'Home'){
          generate_big_screen_binding_structure();
          generate_static_bot_big();
        }
        else if (APP_NAVIGATION[0] == 'About'){
            generate_big_screen_binding_structure();
            generate_static_bot_big();     
        }
        else if (APP_NAVIGATION[0] == 'PromptCheckin'){
          generate_big_screen_prompt_binding_structure();
          generate_prompt_mode();
        }
  
      }
    }
    
}


//component building functions
//small screen binding

function generate_small_screen_binding_stucture(){
    console.log('creating small screen binding structure');
    let small_display_section = document.createElement('div');
    small_display_section.classList.add('small_display_section');
    APP_PARENT_ELEMENT.innerHTML = '';
    APP_PARENT_ELEMENT.appendChild(small_display_section);
  }
  
// big screen dinding
function generate_big_screen_binding_structure(){
    console.log('creating big screen binding structure');
  
    let large_display_section = document.createElement('div');
    large_display_section.classList.add('large_display_section');
    let bot_display_section = document.createElement('div');
    bot_display_section.classList.add('bot_display_section');
  
    APP_PARENT_ELEMENT.innerHTML = ``;
    APP_PARENT_ELEMENT.classList.remove('parent_display_container_prompt');
    APP_PARENT_ELEMENT.classList.add('parent_display_container');
    APP_PARENT_ELEMENT.appendChild(large_display_section);
    APP_PARENT_ELEMENT.appendChild(bot_display_section);
  }

  
function generate_big_screen_prompt_binding_structure(){
    console.log('creating big screen prompt binding structure');
  
    let small_display_section = document.createElement('div');
    small_display_section.classList.add('small_display_section');
  
    APP_PARENT_ELEMENT.innerHTML = ``;
    
    APP_PARENT_ELEMENT.classList.add('parent_display_container_prompt');
  
    APP_PARENT_ELEMENT.appendChild(small_display_section);
  }
  

// bot components section
function get_to_date_string(element_object){
    let d = new Date();
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  
    element_object.innerHTML=`<b>${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}</b>`
  
  }

function generate_bot_app_button_stack(arr){
    console.log(`generate_bot_app_button_stack`);
  
    let button_stack = document.createElement('div');
    button_stack.classList.add('bot_app_button_stack');
  
    console.log(button_stack);
      
    for (let i=0; i<arr.length; i++){
        current_item_split = arr[i].split(":");
        let button = document.createElement('button');
        button.classList.add('b_btn');
        button.classList.add('bot_button');
        let div_row = document.createElement('div');
        div_row.classList.add('row')
      
        div_row.innerHTML = `
          <div class="col-8">
          <span class="type_label">${current_item_split[0]}</span>
      
          </div>
          <div class="col-4">
          <span class="type_label">
      
              <i class="${current_item_split[1]}"></i>
  
          </span>
          </div>
          `
      
        button.appendChild(div_row);
      
        fun = /\w{1,}/.exec(current_item_split[2]);
        fun = fun[0];
          
        if (fun == 'showItemsOfSale') {
            button.addEventListener('click', function() {
                console.log('clicked items button');
            });
        } else if (fun == 'promptBotCheckin') {
            button.addEventListener('click', promptBotCheckin);
        } else if (fun == 'callShop') {
            button.addEventListener('click', callShop);
        } else if (fun == 'mailShop') {
            button.addEventListener('click', mailShop);
        } else if (fun == 'showAboutShop') {
            button.addEventListener('click', function() {
                console.log('clicked about button');
            });
        } else if (fun == 'returnHome') {
            button.addEventListener('click', returnHome);
        } else if (fun == 'refreshDisplay') {
            button.addEventListener('click', refreshDisplay);
        } else if (fun == 'promptScanCheckin'){
            button.addEventListener('click', upload_file);   
        } else if (fun == 'DownloadStamp') {
            button.addEventListener('click', function() {
                console.log('clicked download button');
            });
        } else if (fun == 'validateRedeemCode') {
            button.addEventListener('click', validateRedeemCode);
        }     
          button_stack.appendChild(button);
        }
  
    return button_stack;
  }


  // Navigation functions
  function callShop(){
    let phone_no = '+254703103960';
    window.location = `tel:${phone_no}`;
  }
  
  function mailShop(){
    let shop_email = 'wowza.africa@gmail.com';
    window.location = `mailto:${shop_email}`;
  }

  function returnHome(){
    APP_NAVIGATION=[];
    APP_NAVIGATION.push('Bot');
    APP_CHECKOUT_ITEM = {};
    render_ui()
  
  }

  function promptBotCheckin(){
    APP_NAVIGATION=[];
    APP_NAVIGATION.push('PromptCheckin')
    render_ui()
  }


  function generate_static_bot_big(){
    console.log('creating static bot for big screen');
  
    let bot_container = document.querySelector('.bot_display_section');
    bot_container.innerHTML=``
  
    let bot_app = document.createElement('div');
    bot_app.classList.add('bot_app');
    bot_container.appendChild(bot_app);
  
    let bot_app_screen = document.createElement('div');
    bot_app_screen.classList.add('bot_app_screen');
  
    let img = document.createElement('img');
    img.classList.add('bot_screen');
    img.src = `static/bot_media/wake_up_big.gif`;
    bot_app_screen.appendChild(img)
  
    let bot_header = document.createElement('h5');
    bot_header.classList.add('bot_header');
    get_to_date_string(bot_header)
  
  
    bot_app.appendChild(bot_app_screen);
    bot_app.appendChild(bot_header);
  
    let stack = generate_bot_app_button_stack(['Check-in:fa fa-qrcode:promptBotCheckin()','Refresh:fa fa-refresh:returnHome()']);
    console.log(`created stack is =>  ${stack}`);
    bot_app.appendChild(stack);
    
    let stack2 = generate_bot_app_button_stack(['Mail:fa fa-envelope:mailShop()','About:fa fa-info-circle:showAboutShop()']);
    bot_app.appendChild(stack2);
  
    bot_app.style.position = 'absolute';
    bot_app.style.top = `2.5%`;
    bot_app.style.right = `10%`;
  
    bot_container.appendChild(bot_app);
  
    return bot_container
  
  }
  
  function generate_static_bot_small(){
    console.log('creating static bot for small screen');
  
    let bot_container = document.querySelector('.small_display_section');
    bot_container.innerHTML=``
  
    let bot_app = document.createElement('div');
    bot_app.classList.add('bot_app');
    bot_container.appendChild(bot_app);
  
    let bot_app_screen = document.createElement('div');
    bot_app_screen.classList.add('bot_app_screen');
  
    let img = document.createElement('img');
    img.classList.add('bot_screen');
    img.src = `static/bot_media/wake_up_small.gif`;
    bot_app_screen.appendChild(img)
  
    let bot_header = document.createElement('h5');
    bot_header.classList.add('bot_header');
    get_to_date_string(bot_header)
  
  
    bot_app.appendChild(bot_app_screen);
    bot_app.appendChild(bot_header);
  
    let stack = generate_bot_app_button_stack(['Shopping:fa fa-shopping-cart:showItemsOfSale()', 'Check-in:fa fa-qrcode:promptBotCheckin()']);
    console.log(`created stack is =>  ${stack}`);
    bot_app.appendChild(stack);
    
    let stack2 = generate_bot_app_button_stack(['Call:fa fa-phone:callShop()','Mail:fa fa-envelope:mailShop()','About:fa fa-info-circle:showAboutShop()']);
    bot_app.appendChild(stack2); 
    bot_container.appendChild(bot_app);
  
    return bot_container
  
  }

  async function generate_prompt_mode(){
    console.log( `generating prompt mode for navigation ${APP_NAVIGATION}`);
  
    let bot_container = document.querySelector('.small_display_section');
    bot_container.innerHTML=``
  
    let bot_app = document.createElement('div');
    bot_app.classList.add('bot_app');
    bot_container.appendChild(bot_app);
  
    let bot_app_screen = document.createElement('div');
    bot_app_screen.classList.add('bot_app_screen');
  
    let img = document.createElement('img');
    img.classList.add('bot_screen');
    img.src = `static/bot_media/bot_screen_test.gif`;
    img.style.borderRadius = `15px`;
    bot_app_screen.appendChild(img);
  
    let bot_header = document.createElement('h5');
    bot_header.classList.add('bot_header');
    bot_header.innerHTML=`<b>Check-in</b>`;
  
    let reader_section = document.createElement('span');
    reader_section.setAttribute('id', 'reader');
    reader_section.style.display='none';  
  
  
    bot_app.appendChild(bot_app_screen);
    bot_app.appendChild(bot_header);
    bot_app.appendChild(reader_section)
  
    let stack = generate_bot_app_button_stack(['Upload:fa fa-upload:promptScanCheckin()', 'Cancel:fa fa-times:returnHome()']);
    console.log(`created stack is =>  ${stack}`);
    bot_app.appendChild(stack);
  
  
    return bot_container;
    }
  


  function upload_file(){
    console.log(`${this}`)
    let file_input_el = document.createElement('input');
    file_input_el.setAttribute('type', 'file');
    file_input_el.addEventListener('change', process_ticket_qr);
    file_input_el.click();
  
  }
  
  let scan_res_var = ""
  
  function process_ticket_qr(event) {
    uploadedFile = event.target.files[0];
    generate_prompt_redeem();
  }
  
  
  async function generate_prompt_redeem(redeemCode = null, imgSrc = 'static/bot_media/bot_screen_test.gif'){
    console.log( `generating prompt redeem for navigation ${APP_NAVIGATION}`);
  
    console.log(`redeem code value , ${redeemCode}`)
  
    let bot_container = document.querySelector('.small_display_section');
    bot_container.innerHTML=``
  
    let bot_app = document.querySelector('.small_display_section');
    
    let bot_input_section = document.querySelector('.bot_input_section')
  
    let bot_input_redeem_code = document.createElement('input');
    bot_input_redeem_code.type = 'text';
    bot_input_redeem_code.placeholder = 'REDEEM CODE'
    bot_input_redeem_code.name = 'redeem_code';
  
    bot_input_section.appendChild(bot_input_redeem_code);
  

    bot_app.appendChild(bot_input_section);
  
  
    return bot_container;
  }


  async function generate_prompt_error_input(){
    console.log('calling generate_prompt_error_input')
  }
  
  
  async function validateRedeemCode() {
    let redeemCodeInput = document.querySelector('input[name="redeem_code"]');
    let userInput = redeemCodeInput.value.trim();
  
    if (!userInput) {
      console.log("Redeem code is empty. Please enter a valid redeem code.");
      return;
    }
  
    // Store the redeem code
    redeemCode = userInput;
  
    // Make the final request with the stored data
    let url_string = `${location.origin}/recognize_artifact`;
    var formData = new FormData();
    formData.append('image', uploadedFile);
    formData.append('redeem_code', redeemCode); // Add the redeem code to the form data
  
    fetch(url_string, {
      method: 'POST',
      body: formData
    })
    .then(function(response) {
      if (response.ok) {
        return response.text();
      }
      throw new Error('Error processing image.');
    })
    .then(function(responseText) {
      console.log(`processed successfully ${responseText}`);
      const res_json = JSON.parse(responseText);
      // ... (any further processing you need to do)
    })
    .catch(function(error) {
      console.error(error);
    });
  
  
  
  }
  
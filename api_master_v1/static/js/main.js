
let APP_PARENT_ELEMENT = document.querySelector('.parent_display_container');

window.addEventListener('DOMContentLoaded', function() {  
  refreshDisplay(); 
  setInitialZoom(); // Set the initial zoom level to 90% when the page loads

  // Select all elements with the class "itemForm"
  const itemForms = document.getElementsByClassName("itemForm");

  // Iterate over each element and attach the event listener
  Array.from(itemForms).forEach(function(itemForm) {
    itemForm.addEventListener("submit", function(event) {
      event.preventDefault(); // Prevent the default form submission behavior
    
      // Add your logic here if needed
    
      // For this example, we do nothing after preventing the default behavior
    });
  });


  let botHeader = document.getElementById("botHeader");
  

  get_to_date_string(botHeader);
  
  
});


// Function to set the initial zoom level on page load
function setInitialZoom() {
  // console.log(`zooming`)
  const initialZoom = 0.7; // 80%
  document.documentElement.style.zoom = initialZoom;
}


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

  handle_first_time_contact();
  
  if(getScreenMode() == 'small'){
    console.log('yup, small screen');
    // check auth state in localStorage
    // if auth : [checkin, shop, wallet], [scanner], [call,mail,about]
    // else : [checkin], [scanner], [call,mail,about]
    show_big_screen_context_btns();
  }
  else if (getScreenMode() == 'large'){
    console.log('yup, large screen');
    // check auth state in localStorage
    // if auth : [checkin, shop, wallet], [refresh,scanner], [call, mail, about]
    // else : [checkin], [scanner], [call,mail,about]
    show_big_screen_context_btns();
  }
  
}

// bot components section
function get_to_date_string(element_object){
  console.log("calling get_to_date_string")
  let d = new Date();
  const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  element_object.innerHTML=`<b>${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}</b>`

}

// Get the bot_app element
const botApp = document.querySelector('.bot_app');

// Get the initial offset from the top
const initialOffset = botApp.getBoundingClientRect().top;

// Function to update the position of bot_app for large screens
function updateBotAppPosition() {
  const screenMode = getScreenMode();
  if (screenMode === 'large') {
      const scrollTop = window.scrollY;
      const threshold = 4; // You can adjust this value
      // console.log(`scrollTop value : ${scrollTop}`)
      botApp.style.position = 'absolute';
      botApp.style.top = `${threshold}px`
    
  } 
}

// Add a scroll event listener to update the position during scrolling
window.addEventListener('scroll', updateBotAppPosition);

// Call the function on page load to set the initial position
updateBotAppPosition();



// button functions

function process_button_master(button) {
  console.log('process button master');
  const select_btn = button.id;
  console.log(`selected button is ${select_btn}`);

  // Use a switch statement to handle button-specific logic
  switch (select_btn) {
    case "check_in":
      process_checkin();
      break;
    case "shop":
      process_shop();
      break;
    case "wallet":
      process_wallet();
      break;
    case "refresh":
      process_refresh();
      break;
    case "camera":
      process_camera();
      break;
    case "call":
      process_call();
      break;
    case "mail":
      process_mail();
      break;
    case "about":
      process_about();
      break;
    case "base_cancel":
      process_base_cancel();
      break;
    case "second_cancel":
      process_second_cancel();
      break;
    case "redeem":
      process_checkin_redeem();
      break;
    case "purchase":
      process_checkin_purchase();
      break;
    default:
      console.log(`No handler for button ID: ${select_btn}`);
  }
}



function process_base_cancel(){
  console.log('processing base_cancel');
  // hide info div
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    botInfoDisplay.style.display = "none";

  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    botNavigation.style.display = "none"
  }

  // restore start view
  const botButtonStackBig = document.getElementById("botButtonStackBig");
  botButtonStackBig.style.display = "block";

  const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
  botButtonStackMiddle.style.display = "block";

  const botButtonStackContact = document.getElementById("botButtonStackContact");
  botButtonStackContact.style.display = "block";

}

function process_second_cancel(){
  console.log('process second_cancel');

  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    botInfoDisplay.style.display = "none";

  }

  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    botNavigation.style.display = "none"
  }

  // restore start view
  const botButtonStackBig = document.getElementById("botButtonStackBig");
  botButtonStackBig.style.display = "block";

  const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
  botButtonStackMiddle.style.display = "block";

  const botButtonStackContact = document.getElementById("botButtonStackContact");
  botButtonStackContact.style.display = "block";
  
}

function process_checkin(){
  console.log('process checkin');
  fold_bot_start_display();
  show_checkin_info();
  show_checkin_base_navigation();
}

function process_shop(){
  console.log('process shop');
  fold_bot_start_display();
  show_shop_info();
  show_shop_base_navigation();
}

function process_wallet(){
  console.log('process wallet');
  fold_bot_start_display();
  show_wallet_info();
  show_wallet_base_navigation();
}


function process_camera(){
  console.log('process camera');
  fold_bot_start_display();
  show_scanner_info();
  show_scanner_base_navigation();
}

function process_about(){
  console.log('process about');
  fold_bot_start_display();
  show_about_info();
  show_about_base_navigation();
}


function process_refresh(){
  console.log('process refresh')
}


function process_call(){
  console.log('process call');
  // prompt call from device
  // Assuming you want to initiate a phone call, you can use the `tel:` protocol to prompt a call on mobile devices
  const phoneNumber = "254703103960"; // Example phone number, replace with dynamic data if needed
  window.location.href = `tel:${phoneNumber}`; // This will prompt the device to make a call to the provided number
}

function process_mail(){
  console.log('process mail');
  // prompt mail from device
  const subject = "Reach from Customer";
  const body = "Body content goes here";
  const recipient = "otienot75@gmail.com"; // Fixed recipient email address

  // Use the mailto protocol to open the default email client with the recipient, subject, and body
  window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  // This will open the default email client with the provided subject, body, and recipient email address pre-filled.
}

// checkin redeem

function process_checkin_redeem(){
  console.log('process checkin redeem option')

  fold_bot_start_display();
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }
  show_checkin_reddem_info();
  show_checkin_redeem_navigation();
}


function process_checkin_purchase(){
  console.log('process checkin purchase option')

  fold_bot_start_display();
  const botInfoDisplay = document.getElementById('botInfoDisplay');
  if (botInfoDisplay){
    botInfoDisplay.innerHTML='';
    
  }
  // hide nav giv
  const botNavigation = document.getElementById("botNavigation");
  if (botNavigation){
    botNavigation.innerHTML='';
    
  }

  show_checkin_purchase_info();
  show_checkin_purchase_navigation();

}



// minima stuff
MDS.init(function(msg) {
  switch (msg.event) {
      case "inited":
          MDS.log("MDS has been initialised.");
          break;
      case "NEWBALANCE":
          MDS.log("New balance: " + JSON.stringify(msg.data));
          break;
      case "NEWBLOCK":
          MDS.log("New block: " + JSON.stringify(msg.data));
          break;
      case "MINING":
          MDS.log("Mining status: " + JSON.stringify(msg.data));
          break;
      case "MINIMALOG":
          MDS.log("Log message: " + JSON.stringify(msg.data));
          break;
      case "MAXIMA":
          MDS.log("Maxima message: " + JSON.stringify(msg.data));
          break;
      case "MDS_TIMER_1HOUR":
          MDS.log("One-hour timer event.");
          break;
      case "MDS_TIMER_10SECONDS":
          MDS.log("10-second timer event.");
          MDS.notify("This is a notification message.");
          MDS.notifycancel();
          break;
      case "MDS_SHUTDOWN":
          MDS.log("System shutdown message received.");
          break;
  }
});


function generate_first_auth_unique_id() {
  console.log('calling generate_first_auth_unique_id');
  const sessionObj = {
      is_active: false,
      id: generateUniqueId(),
      created_at: Date.now().toString(),
      updated_at: Date.now().toString(),
      ttl: '',
      user_type: 'first'
  };
  persist(sessionObj.id, sessionObj);
  return JSON.stringify(sessionObj);
}

function generate_customer_auth_unique_id() {
  console.log('calling generate_customer_auth_unique_id');
  const sessionObj = {
      is_active: false,
      id: generateUniqueId(),
      created_at: Date.now().toString(),
      updated_at: Date.now().toString(),
      ttl: '',
      user_type: 'customer'
  };
  persist(sessionObj.id, sessionObj);
  return JSON.stringify(sessionObj);
}

function generate_vendor_auth_unique_id() {
  console.log('calling generate_vendor_auth_unique_id');
  const sessionObj = {
      is_active: false,
      id: generateUniqueId(),
      created_at: Date.now().toString(),
      updated_at: Date.now().toString(),
      ttl: '',
      user_type: 'vendor'
  };
  persist(sessionObj.id, sessionObj);
  return JSON.stringify(sessionObj);
}


function add_session_ttl(user_type) {
  console.log('calling add_session_ttl');
  let ttlHours;

  switch (user_type) {
      case 'first':
          ttlHours = 1; // 1 hour
          break;
      case 'customer':
          ttlHours = 48; // 48 hours
          break;
      case 'vendor':
          ttlHours = 72; // 72 hours
          break;
      default:
          console.error('Invalid user type');
          return 0;
  }

  return ttlHours * 60 * 60 * 1000; // Convert hours to milliseconds
}



function persist(key, sessionObj) {
  console.log('calling persist');
  try {
      localStorage.setItem(key, JSON.stringify(sessionObj));
      console.log(`Session saved for key: ${key}`);
  } catch (error) {
      console.error('Error saving session to localStorage', error);
  }
}


function determine_user_session_ttl(userId) {
  console.log('calling determine_user_session_ttl');
  const sessionData = localStorage.getItem(userId);

  if (!sessionData) {
      console.error('Session not found');
      return -1;
  }

  const sessionObj = JSON.parse(sessionData);
  const currentTime = Date.now();
  const sessionExpiry = parseInt(sessionObj.created_at) + parseInt(sessionObj.ttl);

  if (currentTime >= sessionExpiry) {
      console.log('Session has expired');
      return 0;
  }

  const remainingTtl = sessionExpiry - currentTime;
  console.log(`Remaining TTL for session ${userId}: ${remainingTtl} ms`);
  return remainingTtl;
}


function generateUniqueId() {
  return [...Array(32)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');
}


function handle_first_time_contact() {
  console.log('Handling first-time contact');

  // Iterate through all keys in localStorage to find session data
  const sessionKeys = Object.keys(localStorage);
  let activeSession = null;

  for (const key of sessionKeys) {
      const sessionData = localStorage.getItem(key);
      if (sessionData) {
          const sessionObj = JSON.parse(sessionData);

          // Check if session has `user_type` attribute to validate it's a session object
          if (sessionObj.user_type) {
              const ttlStatus = determine_user_session_ttl(sessionObj.id);

              if (ttlStatus > 0) {
                  console.log('Active session found:', sessionObj);
                  activeSession = sessionObj;
                  break;
              } else {
                  console.log('Session expired. Clearing session:', sessionObj.id);
                  localStorage.removeItem(sessionObj.id);
              }
          }
      }
  }

  if (!activeSession) {
      console.log('No active session found or session expired. Regenerating first session.');
      const newSession = JSON.parse(generate_first_auth_unique_id());
      newSession.ttl = add_session_ttl(newSession.user_type);
      persist(newSession.id, newSession);

      console.log('New session created:', newSession);
      return newSession;
  }

  console.log('Using existing active session:', activeSession);
  return activeSession;
}

function createSession(userType, isActive, ttlOffsetInHours) {
  const now = Date.now();
  const session = {
      is_active: isActive,
      id: `${userType}_${Math.random().toString(36).substr(2, 16)}`,
      user_type: userType,
      created_at: now.toString(),
      updated_at: now.toString(),
      ttl: (now + ttlOffsetInHours * 60 * 60 * 1000).toString()
  };
  localStorage.setItem('user_session', JSON.stringify(session));
  console.log(`Session created: ${JSON.stringify(session, null, 2)}`);
} 

function is_active() {
  console.log('calling is_active');

  // Check if there is any active session in localStorage
  const sessionKeys = Object.keys(localStorage);

  for (const key of sessionKeys) {
      const sessionData = localStorage.getItem(key);
      if (sessionData) {
          const sessionObj = JSON.parse(sessionData);

          if (sessionObj.is_active) {
              console.log(`Active session found: ${key}`);
              return true;
          }
      }
  }

  console.log('No active session found.');
  return false;
}

function is_first() {
  console.log('calling is_first');

  // Iterate through sessions to check if there's a "first" session
  const sessionKeys = Object.keys(localStorage);

  for (const key of sessionKeys) {
      const sessionData = localStorage.getItem(key);
      if (sessionData) {
          const sessionObj = JSON.parse(sessionData);

          if (sessionObj.user_type === 'first') {
              console.log(`'First' session found: ${key}`);
              return true;
          }
      }
  }

  console.log('No session with user_type "first" found.');
  return false;
}

function is_customer() {
  console.log('calling is_customer');

  // Iterate through sessions to check if there's a "customer" session
  const sessionKeys = Object.keys(localStorage);

  for (const key of sessionKeys) {
      const sessionData = localStorage.getItem(key);
      if (sessionData) {
          const sessionObj = JSON.parse(sessionData);

          if (sessionObj.user_type === 'customer') {
              console.log(`'Customer' session found: ${key}`);
              return true;
          }
      }
  }

  console.log('No session with user_type "customer" found.');
  return false;
}

function is_vendor() {
  console.log('calling is_vendor');

  // Iterate through sessions to check if there's a "vendor" session
  const sessionKeys = Object.keys(localStorage);

  for (const key of sessionKeys) {
      const sessionData = localStorage.getItem(key);
      if (sessionData) {
          const sessionObj = JSON.parse(sessionData);

          if (sessionObj.user_type === 'vendor') {
              console.log(`'Vendor' session found: ${key}`);
              return true;
          }
      }
  }

  console.log('No session with user_type "vendor" found.');
  return false;
}



function process_render() {
  console.log('calling process_render');

  if (is_active()){
    console.log('active user\n\n');

    if (is_first()){
      console.log('is first user');
      show_first_active();
    }

    if(is_customer()){
      console.log('is customer user');
      show_customer_active();
    }

    if(is_vendor()){
      console.log('is vendor user');
      show_vendor_active();
    }
  }
  else{
    console.log('inactive user\n\n')

    if (is_first()){
      console.log('is first user');
      show_first_inactive();

    }

    if(is_customer()){
      console.log('is customer user ')
      show_customer_inactive();
    }

    if(is_vendor()){
      console.log('is vendor user')
      show_current_inactive();
    }
  }
}



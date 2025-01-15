// Mock data

// always update on page refresh
const sessionData = {
    activity_json: {
        current_intent: 'Landing_page'
    }
};

// const resourceData = [
//     { id: 1, public: true, item_media_url: 'landing_images/sample3.jpg', title: 'Item 1', price: 100, name: 'Item One', description: 'Description of Item One' },
//     { id: 2, public: true, item_media_url: 'landing_images/sample4.jpg', title: 'Item 2', price: 200, name: 'Item Two', description: 'Description of Item Two' },
//     { id: 3, public: true, item_media_url: 'landing_images/doom.jpeg', title: 'Item 3', price: 200, name: 'Item Three', description: 'Description of Item Three' }
// ];



const items_of_sale = [
    [
        // shop items
        {   id: 1, 
            public:true, 
            item_media_url: 'landing_images/subscription_box.jpg', 
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title: 'Subscription Box', 
            price: 100, 
            name: 'Electronics Box', 
            description: 'Subscribe today and get the latest information and offers for your electronic products' ,
            item_type:"shopping",
            view_type:"pu_pr"
        },
        {   id: 2, 
            public:true, 
            item_media_url: 'landing_images/bender.jpg', 
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title: 'Subscription Box', 
            price: 100, 
            name: 'Marijuana Box', 
            description: 'Subscribe today and get the latest information and offers for your weed products' ,
            item_type:"physical",
            view_type:"pr"
        },
        {   id: 3, 
            public:true, 
            item_media_url: 'landing_images/bunny.jpg', 
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title: 'Subscription', 
            price: 100, 
            name: 'Playboy Bunny', 
            description: 'Subscribe today and get the latest information and offers for your playboy products' ,
            item_type:"physical",
            view_type:"pr"
        },
        
    ],
    [
        // game items
        {
            id:12,
            public:true,
            item_media_url:"landing_images/gba_super_mario.jpeg",
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title:"Game Boy Advance",
            price:0,
            name: "Mario",
            description: "Enjoy The Classic Mario Game",
            item_type:"game_boy_advance",
            view_type:"pu_pr"
        },
        {
            id:10,
            public:true,
            item_media_url:"landing_images/gba_mortal_kombat_deadly_alliance.jpg",
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title:"Game Boy Advance",
            price:0,
            name: "Mortal Kombat",
            description: "Enjoy The Classic Mortal Kombat Daily Alliance",
            item_type:"game_boy_advance",
            view_type:"pu_pr"
        },
        {
            id:11,
            public:true,
            item_media_url:"landing_images/gba_the_last_air_bender.jpeg",
            item_insta_card_big_url: "",
            item_insta_card_small_url: "",
            item_order_card_url: "",
            item_receipt_card_url: "",
            title:"Game Boy Advance",
            price:0,
            name: "Avatar The Last Air Bender",
            description: "Enjoy The Classic Air Bender",
            item_type:"game_boy_advance",
            view_type:"pu_pr"
        }
        
    ]
    
];


function add_items_of_sale(){
    console.log('calling add_items_of_sale')
}
    

const botView = {
    current_bot_screen_media: ['./static/bot_media/wake_up_big.gif', './static/bot_media/wake_up_small.gif'],
    current_bot_buttons: [
        [
            { id: 'check_in', label: 'Check-in', icon: 'fa-solid fa-right-to-bracket' },
            { id: 'shop', label: 'Shop', icon: 'fa-brands fa-searchengin' },
            { id: 'wallet', label: 'Wallet', icon: 'fa-solid fa-wallet' }
        ],
        [
            { id: 'call', label: 'Call', icon: 'fa-solid fa-phone' },
            { id: 'mail', label: 'Mail', icon: 'fa-solid fa-envelope' },
            { id: 'about', label: 'About', icon: 'fa-solid fa-info-circle' }
        ]
    ],

    current_first_middle_buttons: [
        { id: 'check_in', label: 'Check-in', icon: 'fa-solid fa-right-to-bracket' },
        { id: 'shop', label: 'Shop', icon: 'fa-brands fa-searchengin' },
    ],

    current_bot_customer_inactive_buttons: [
        
        { id: 'shop', label: 'Shop', icon: 'fa-brands fa-searchengin' },
    ],

    current_bot_customer_active_buttons:[
        { id: 'check_in', label: 'Check-in', icon: 'fa-solid fa-right-to-bracket' },
        { id: 'shop', label: 'Shop', icon: 'fa-brands fa-searchengin' },
        { id: 'wallet', label: 'Wallet', icon: 'fa-solid fa-wallet' }
    ],


    current_middle_button: [
        [
            { id: 'refresh', label: 'Refresh', icon: 'fa-solid fa-refresh' },
            { id: 'camera', label: 'Capture', icon: 'fa-solid fa-camera' },
            { id: 'games', label: 'Games', icon: 'fa-solid fa-gamepad' },
            { id: 'smarttv', label: 'Stream', icon: 'fa-solid fa-display' }
        ]
    ],

    current_bot_middle_customer_active_buttons:[
        { id: 'camera', label: 'Scanner', icon: 'fa-solid fa-camera' },
        { id: 'smarttv', label: 'Watch', icon: 'fa-solid fa-display' }
    ],

    current_bot_middle_customer_inactive_buttons: [
        { id: 'camera', label: 'Scanner', icon: 'fa-solid fa-camera' },
        { id: 'games', label: 'Games', icon: 'fa-solid fa-gamepad' }
    ],

    
    
    current_checkin_base_buttons: [
        { id: 'redeem', label: 'Redeem', icon: 'fa-solid fa-gift' },
        { id: 'purchase', label: 'Purchase', icon: 'fa-solid fa-money-bill-wave'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_checkin_info:{
        title: "Authentication",
        content: "Inorder to access more features, authenticate yourself by entering redeem code or purchasing a session of your interest"
    },

    current_shop_base_buttons : [
        { id: 'update_location', label: 'Location', icon: 'fa-solid fa-location-crosshairs'},
        { id: 'shop_cart', label: 'Cart', icon: 'fa-solid fa-cart-shopping' },
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_shop_info: {
        title: "Shopping",
        content: 'Shopping information'
    },

    current_shop_base_0_buttons: [
        { id: 'update_location', label: 'Location', icon: 'fa-solid fa-location-crosshairs'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_shop_base_0_active_buttons: [
        { id: 'update_location', label: 'Location', icon: 'fa-solid fa-location-crosshairs'},
        { id: 'cancel_location', label: 'Stop Track', icon: 'fa-solid fa-ban' },
        { id: 'proceed_shopping', label: 'Proceed', icon: 'fa-solid fa-arrow-right'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_shop_base_0_info: {
        title: "Shopping 0",
        content: "Shopping 0 Information"
    },

    current_shop_base_1_buttons: [
        { id: 'proceed_shopping', label: 'Proceed', icon: 'fa-solid fa-arrow-right'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_shop_base_1_info: {
        title: "Shopping 1",
        content: "Shopping 1 Information"
    },

    current_pu_pr_buttons: [
        { id: "pu_pr_online", label: 'Online', icon: 'fa-solid fa-globe'},
        { id: "pu_pr_physical", label: "Physical", icon: 'fa-solid fa-door-open'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_pu_pr_info : {
        title: "Select Service",
        content: "Pu_PR content"
    },

    current_pu_buttons : [
        { id: "pu_online", label: "Online", icon: "fa-solid fa-globe"},
        { id: "pu_physical", label: "Physical", icon: "fa-solid fa-cart-shopping"},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_pu_info : {
        title: "Select Service",
        content: "Pu content"
    },

    current_wallet_base_buttons: [
        { id: 'mpesa', label: 'Mpesa', icon: 'fa-solid fa-money-bill'},
        { id: 'blockchain_minima', label: 'Minima', icon: 'fa-solid fa-bolt-lightning'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_wallet_info : {
        title: "Wallet",
        content: "Our wallet allows you keep track of money and points when you shop and participate in other activities in the bot"
    },

    current_scanner_base_buttons: [
        { id: 'take_photo', label: 'Camera', icon: 'fa-solid fa-camera'},
        { id: 'scan_media', label: 'Scanner', icon: 'fa-solid fa-upload'},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_scanner_info : {
        title: "Scanner",
        content: "Our scanner allows you to take pictures, scan qr codes and also pdfs"
    },

    current_scanner_capture_base_buttons : [
        // { id: 'start', label: 'Start', icon: "fa-solid fa-camera-rotate"},
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_about_base_buttons : [
        { id: 'base_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_about_info:{
        title: "About",
        content: "K-VCR is a series bot, designed to help you achieve essential utilities while on the  internet"
    },

    current_checkin_redeem_buttons : [
        { id: 'checkin_redeem_copy', label: 'Paste', icon: 'fa-solid fa-paste'},
        { id: 'checkin_redeem_clear', label: 'Clear', icon: 'fa-solid fa-eraser'},
        { id: 'checkin_redeem_submit', label: 'Submit', icon: 'fa-solid fa-arrow-right'},
        { id: 'second_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_checkin_redeem_info: {
        title: "Redeem",
        content: "Redeem Session by pasting the code you recieved, generated by our system, select the session first",
        input : [
            {type:'select', list: [
                {label: 'customer', value: 'select_customer'},
                {label:'vendor', value:'select_vendor'}
            ]}
        ]
    },

    current_checkin_purchase_buttons : [
        { id: 'checkin_purchase_copy', label: 'Paste', icon: 'fa-solid fa-paste'},
        { id: 'checkin_purchase_clear', label: 'Clear', icon: 'fa-solid fa-eraser'},
        { id: 'checkin_purchase_submit', label: 'Submit', icon: 'fa-solid fa-arrow-right'},
        { id: 'second_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    current_checkin_purchase_info: {
        title: "Purchase",
        content: "Purchase session using Mpesa,select the type of session first",
        input: [
            {type:'select', list: [
                {label: 'customer', value: 'select_customer'},
                {label:'vendor', value:'select_vendor'}
            ]}
        ]
    },

    current_checkin_redeem_success_result_info: {
        title: "Success!",
        content: "Your session is now active, press done to proceed",
    },

    current_checkin_redeem_success_buttons: [
        { id: 'done', label: 'Done', icon: 'fa-solid fa-check'}
    ],

    current_checkin_redeem_fail_result_info: {
        title: "Failed!",
        content: "Your session was unable to redeem, please try again"
    },

    current_checkin_redeem_fail_buttons: [
        { id: 'retry_checkin_redeem', label: 'Retry', icon: 'fa-solid fa-arrow-rotate-right'},
        { id: 'second_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],


    current_checkin_purchase_success_result_info: {
        title: "Success!",
        content: "Your session is now active, press done to proceed",
    },

    current_checkin_purchase_success_buttons: [
        { id: 'done', label: 'Done', icon: 'fa-solid fa-check'}
    ],

    current_checkin_purchase_fail_result_info: {
        title: "Failed!",
        content: "Your session was unable to redeem, please try again"
    },

    current_checkin_purchase_fail_buttons: [
        { id: 'retry_checkin_purchase', label: 'Retry', icon: 'fa-solid fa-arrow-rotate-right'},
        { id: 'second_cancel', label: 'Cancel', icon: 'fa-solid fa-rectangle-xmark'}
    ],

    landing_game_screen_media:[
        './static/bot_media/gameboyadvance_image.jpg'
    ],

    landing_game_top_buttons: [
        { id: 'free_games', label: 'Free Games', icon: 'fa-solid fa-smile'},
        { id: 'load_game', label: 'Load Game', icon: 'fa-solid fa-floppy-disk'}
    ],

    landing_game_middle_buttons:[
        { id: 'select_game', label:'Select', icon: 'fa-solid fa-arrow-right'},
        { id: 'start_game', label:'Start', icon:'fa-solid fa-check'}
    ],

    landing_game_gba_buttons:[
       
            { id: 'gba_left', label: '.', icon: 'fa-solid fa-caret-left'},
            { id: 'gba_right', label: '.', icon: 'fa-solid fa-caret-right'},
            { id: 'gba_up', label: '.', icon: 'fa-solid fa-caret-up'},
            { id: 'gba_down', label: '.', icon: 'fa-solid fa-caret-down'},
          
            { id: 'gba_l', label: 'L', icon: 'fa-solid fa-l'},
            { id: 'gba_r', label: 'R', icon: 'fa-solid fa-r'},
            { id: 'gba_a', label: 'A', icon: 'fa-solid fa-a'},
            { id: 'gba_b', label: 'B', icon: 'fa-solid fa-b'},
        
        
    ],

    landing_game_extra_buttons:[
        { id: 'exit_gba', label: 'Exit', icon:'fa-solid fa-circle-xmark'}
    ]

};

    
function show_new_items_of_sale(){
    console.log("show_new_items_of_sale called")
    const itemCardContainer = document.getElementById('itemCardContainer');
    items_of_sale[0].forEach(item => {
        if (item.public) {
            const card = document.createElement('div');
            card.classList.add('item_card');
            card.innerHTML = `
                <img class="item_card_image" src="./static/media_store/${item.item_media_url}" alt="${item.title}">
                <div class="item_info">
                    <div class="item_info_title">
                        <h3 class="item_title">${item.title}</h3>
                        <p class="item_price">Ksh ${item.price}</p>
                    </div>
                    <p class="item_name">${item.name}</p>
                    <p class="item_description">${item.description}</p>
                </div>
                <form class="item_get_button_layer itemForm">
                    <input type="hidden" name="make_order_item_id" value="${item.id}">
                    <button class="item_get_button">Get</button>
                </form>
            `;
            itemCardContainer.appendChild(card);
        }
    });
}

function update_items_of_sale_view(){
    console.log('\ncalling update_items_of_sale_view\n');

    // check if pr_activated
    const pr_activated = check_pr_activated();

    if (pr_activated === true){
        console.log('pr_activated is true')
        view_type = "pu_pr";
    }
    else{
        console.log('pr_activated is false')
        view_type = "pu";
    }

    screen_mode = getScreenMode();

    if (screen_mode === "large"){
        if (view_type === "pu_pr"){
            console.log('rendering pu_pr in large screen')
        }
        else{
            console.log('rendering pu in large screen')
        }
    }
    else {
        if (view_type === "pu_pr"){
            console.log('rendering pu_pr in small screen')
        }
        else{
            console.log('rendering pu in small screen')
        }
    }
}


function render_pu_pr_online_items_of_sale(){
    console.log('rendering pu_pr online items')
}

function render_pu_online_items_of_sale(){
    console.log('rendering pu online items')
}

function render_pu_pr_physical_items_of_sale(){
    console.log('rendering pu_pr physical items')
}

function render_pu_physical_items_of_sale(){
    console.log('rendering pu physical items')
}

function show_remaining_buttons(){
    console.log('showing remianing buttons')

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');

    botView.current_middle_button[0].forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');

    botView.current_bot_buttons[1].forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });

}

function show_big_screen_context_btns(){
    console.log('showing additional buttons for big screen bot');
    // show expected layout
    // populate item cards
    // show_new_items_of_sale()
    update_items_of_sale_view();

    // Populate the bot screen and buttons
    document.getElementById('botScreenBig').src = botView.current_bot_screen_media[1];
       

    process_render()
}

function show_first_active(){
    console.log('calling show_first_active');

    const botButtonStackBig = document.getElementById('botButtonStackBig');

    botButtonStackBig.innerHTML=""
    
    top_button_list = botView.current_first_middle_buttons
    console.log(`current bot_list is ${top_button_list}`)

    
    top_button_list.forEach(button => {
        const buttonBig = document.createElement('div')
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
            <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;
        botButtonStackBig.appendChild(buttonBig);
    });

    middle_button_list = [botView.current_middle_button[0][1], botView.current_middle_button[0][2] ];

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');
    botButtonStackMiddle.innerHTML=""

    middle_button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');
    botButtonStackContact.innerHTML=""

    const contact_button_list = botView.current_bot_buttons[1]

    contact_button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });

}

function show_first_inactive(){
    console.log('calling show_first_inactive');

    const botButtonStackBig = document.getElementById('botButtonStackBig');

    botButtonStackBig.innerHTML=""
    
    top_button_list = botView.current_first_middle_buttons
    console.log(`current bot_list is ${top_button_list}`)

    
    top_button_list.forEach(button => {
        const buttonBig = document.createElement('div')
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
            <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;
        botButtonStackBig.appendChild(buttonBig);
    });

    middle_button_list = [ botView.current_middle_button[0][1], botView.current_middle_button[0][2], botView.current_middle_button[0][3]];

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');
    botButtonStackMiddle.innerHTML=""

    middle_button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');
    botButtonStackContact.innerHTML=""

    const contact_button_list = botView.current_bot_buttons[1]

    contact_button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });

}

function show_customer_active(){
    console.log('calling show_customer_active');

    const botButtonStackBig = document.getElementById('botButtonStackBig');
    botButtonStackBig.innerHTML=""
    
    button_list = botView.current_bot_customer_active_buttons

    button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
            <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;
        botButtonStackBig.appendChild(buttonBig);
    });

    button_list2 = botView.current_bot_middle_customer_active_buttons

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');
    botButtonStackMiddle.innerHTML = ""

    button_list2.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');
    botButtonStackContact.innerHTML = ""

    botView.current_bot_buttons[1].forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });
}

function show_customer_inactive(){
    console.log('calling show_customer_inactive');

    const botButtonStackBig = document.getElementById('botButtonStackBig');
    botButtonStackBig.innerHTML=""
    
    button_list = botView.current_bot_customer_inactive_buttons

    button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
            <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;
        botButtonStackBig.appendChild(buttonBig);
    });

    button_list2 = botView.current_bot_middle_customer_inactive_buttons

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');
    botButtonStackMiddle.innerHTML = ""

    button_list2.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');
    botButtonStackContact.innerHTML = ""

    botView.current_bot_buttons[1].forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });
    
}


function show_vendor_active(){
    console.log('calling show_vendor_active');

    const botButtonStackBig = document.getElementById('botButtonStackBig');
    botButtonStackBig.innerHTML=""
    
    button_list = botView.current_bot_buttons[0]

    button_list.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
            <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;
        botButtonStackBig.appendChild(buttonBig);
    });

    button_list2 = botView.current_middle_button[0]

    const botButtonStackMiddle = document.getElementById('botButtonStackMiddle');
    botButtonStackMiddle.innerHTML=""

    button_list2.forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class="${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackMiddle.appendChild(buttonBig);
    });

    const botButtonStackContact = document.getElementById('botButtonStackContact');
    botButtonStackContact.innerHTML=""

    botView.current_bot_buttons[1].forEach(button => {
        const buttonBig = document.createElement('div');
        buttonBig.classList.add('bot_button_layer');
        buttonBig.innerHTML = `
        <input type="hidden" name="intent" value="${button.label}">
            <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                <div class="row">
                    <div class="col-8">
                        <span class="type-label">${button.label}</span>
                    </div>
                    <div class="col-4">
                        <span class="type_label"><i class=" ${button.icon}"></i></span>
                    </div>
                </div>
            </button>
        `;

        botButtonStackContact.appendChild(buttonBig);
    });
    
}

function show_vendor_inactive(){
    console.log('calling show_vendor_inactive');
    show_first_active();
}

function fold_bot_start_display() {
    console.log('folding bot');

    // Hide botButtonStackBig
    const botButtonStackBig = document.getElementById("botButtonStackBig");
    if (botButtonStackBig) {
        botButtonStackBig.style.display = "none";
        console.log("Hidden botButtonStackBig");
    } else {
        console.log("botButtonStackBig element not found");
    }

    // Hide botButtonStackMiddle
    const botButtonStackMiddle = document.getElementById("botButtonStackMiddle");
    if (botButtonStackMiddle) {
        botButtonStackMiddle.style.display = "none";
        console.log("Hidden botButtonStackMiddle");
    } else {
        console.log("botButtonStackMiddle element not found");
    }

    // Hide botButtonStackContact
    const botButtonStackContact = document.getElementById("botButtonStackContact");
    if (botButtonStackContact) {
        botButtonStackContact.style.display = "none";
        console.log("Hidden botButtonStackContact");
    } else {
        console.log("botButtonStackContact element not found");
    }
}


function show_checkin_base_navigation(){
    console.log('calling checkin base navigation button');
    // change botNavigation to block
    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_checkin_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }

    
}

function show_checkin_info(){
    console.log('calling show_checkin_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_checkin_info.title}</h5>
        <p class="bot_header">${botView.current_checkin_info.content}</p>
        `
    }

}

function show_shop_base_navigation(){
    console.log('calling show_shop_base_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_shop_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }


}


function show_shop_info(){
    console.log('calling show_shop_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_shop_info.title}</h5>
        <p class="bot_header">${botView.current_shop_info.content}</p>
        `
    }
}


function show_shop_base_0_info(){
    console.log('calling show_shop_base_0_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_shop_base_0_info.title}</h5>
        <p class="bot_header">${botView.current_shop_base_0_info.content}</p>
        `
    }
}

function show_shop_base_0_navigation(){
    console.log('calling show_shop_base_0_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_shop_base_0_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}



function show_shop_base_1_info(){
    console.log('calling show_shop_base_1_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_shop_base_1_info.title}</h5>
        <p class="bot_header">${botView.current_shop_base_1_info.content}</p>
        `
    }
}

function show_shop_base_1_navigation(){
    console.log('calling show_shop_base_1_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_shop_base_1_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }

}


function show_pu_pr_info(){
    console.log('calling show_pu_pr_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_pu_pr_info.title}</h5>
        <p class="bot_header">${botView.current_pu_pr_info.content}</p>
        `
    }
}

function show_pu_pr_navigation(){
    console.log('calling show_pu_pr_navigation');

    const botNavigation = document.getElementById("botNavigation");
    botNavigation.innerHTML="";

    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_pu_pr_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}


function show_pu_info(){
    console.log('calling show_pu_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_pu_info.title}</h5>
        <p class="bot_header">${botView.current_pu_info.content}</p>
        `
    }
}

function show_pu_navigation(){
    console.log('calling show_pu_navigation');

    const botNavigation = document.getElementById("botNavigation");
    botNavigation.innerHTML = "";

    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_pu_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}



function show_wallet_base_navigation(){
    console.log('calling show_wallet_base_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_wallet_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}

function show_wallet_info(){
    console.log('calling show_wallet_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_wallet_info.title}</h5>
        <p class="bot_header">${botView.current_wallet_info.content}</p>
        `
    }

}


function show_scanner_base_navigation(){
    console.log('calling show_scanner_base_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_scanner_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}


function show_scanner_info(){
    console.log('calling show_scanner_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_scanner_info.title}</h5>
        <p class="bot_header">${botView.current_scanner_info.content}</p>
        `
    }

}

function show_camera_screen_navigation(){
    console.log('calling show_camera_screen_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botNavigation.innerHTML = "";

        botView.current_scanner_capture_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }

}

function show_camera_screen(){
    console.log('calling show_camera_screen');

    const botInfoDisplay = document.getElementById("botInfoDisplay");

    if(botInfoDisplay){
        // show feed for selected camera
        botInfoDisplay.innerHTML="";

        botInfoDisplay.innerHTML = `
            <div id="reader" width="600px">
            </div>
        `
    }
}

function show_about_base_navigation(){
    console.log('calling show_about_base_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_about_base_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}


function show_about_info(){
    console.log('calling show_about_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_about_info.title}</h5>
        <p class="bot_header">${botView.current_about_info.content}</p>
        `
    }
}


// Function to render the navigation buttons
function show_checkin_redeem_navigation() {
    console.log('calling show_checkin_redeem_navigation');

    const botNavigation = document.getElementById("botNavigation");
    if (botNavigation) {
        botNavigation.style.display = "block";

        // Clear previous buttons if any
        botNavigation.innerHTML = "";

        botView.current_checkin_redeem_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });
    }
}


// Function to render the checkin/redeem info display
function show_checkin_redeem_info() {
    console.log('calling show_checkin_redeem_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if (botInfoDisplay) {
        botInfoDisplay.style.display = "block";

        // Generate the select options
        const options = botView.current_checkin_redeem_info.input[0].list
            .map(option => `<option value="${option.value}" class="select_option">${option.label}</option>`)
            .join('');

        // Update the botInfoDisplay
        botInfoDisplay.innerHTML = `
            <h5 class="bot_header">${botView.current_checkin_redeem_info.title}</h5>
            <p class="bot_header">${botView.current_checkin_redeem_info.content}</p>
            <br>
            
            <input 
                id="redeemInput" 
                placeholder="Code will appear here" 
                disabled 
                class="redeemInput"
            />
            <br>
            <br>
            <br>
        `;
    }
}


// Function to handle the "Paste" button logic
function pasteRedeemCodeToInput() {
    console.log('Paste button clicked');

    const inputField = document.getElementById('redeemInput');

    if (inputField) {
        // Check if the Clipboard API is available
        if (navigator.clipboard && navigator.clipboard.readText) {
            navigator.clipboard.readText()
                .then(clipboardText => {
                    inputField.value = clipboardText; // Populate the input field with clipboard data
                    console.log('Clipboard data pasted:', clipboardText);
                })
                .catch(err => {
                    console.error('Failed to read clipboard data:', err);
                    inputField.value = 'Error: Unable to paste data';
                });
        } else {
            console.error('Clipboard API not supported');
            inputField.value = 'Error: Clipboard not supported';
        }
    }
}

function clear_redeem_paste() {
    console.log('Calling clear_redeem_paste');
    
    const inputField = document.getElementById('redeemInput');
    
    if (inputField) {
        inputField.value = ''; // Clear the input field value
        console.log('Redeem input field cleared');
    } else {
        console.error('Redeem input field not found');
    }
}


function pastePurchaseCodeInput() {
    console.log('Paste button clicked for purchase');

    const inputField = document.getElementById('purchaseInput');

    if (inputField) {
        if (navigator.clipboard && navigator.clipboard.readText) {
            navigator.clipboard.readText()
                .then(clipboardText => {
                    inputField.value = clipboardText;
                    console.log('Clipboard data pasted:', clipboardText);
                })
                .catch(err => {
                    console.error('Failed to read clipboard data:', err);
                    inputField.value = 'Error: Unable to paste data';
                });
        } else {
            console.error('Clipboard API not supported');
            inputField.value = 'Error: Clipboard not supported';
        }
    }
}

function clear_purchase_paste(){
    console.log(`calling clear_purchase_paste`);
    const inputField = document.getElementById('purchaseInput');
    if (inputField) {
        inputField.value = ''; // Clear the input field value
        console.log('Purchase input field cleared');
    } else {
        console.error('Purchase input field not found');
    }
}


// Adjust the height of the textarea dynamically
function adjustTextareaHeight(textarea) {
    textarea.style.height = 'auto'; // Reset height to recalculate
    textarea.style.height = textarea.scrollHeight + 'px'; // Set new height
}


function show_checkin_purchase_navigation(){
    console.log('calling show_checkin_purchase_navigation')

    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_checkin_purchase_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }

}


function show_checkin_purchase_info() {
    console.log('calling show_checkin_purchase_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if (botInfoDisplay) {
        botInfoDisplay.style.display = "block";

        // Generate the select options
        const options = botView.current_checkin_purchase_info.input[0].list
            .map(option => `<option value="${option.value}" class="select_option">${option.label}</option>`)
            .join('');

        // Update the botInfoDisplay
        botInfoDisplay.innerHTML = `
            <h5 class="bot_header">${botView.current_checkin_purchase_info.title}</h5>
            <p class="bot_header">${botView.current_checkin_purchase_info.content}</p>
            
            <br>
            <br>
            <input 
                id="purchaseInput" 
                class="redeemInput" 
                placeholder="Message will appear here" 
                disabled
            >
            <br>
            <br>
            <br>
        `;
    }
}

function show_checkin_redeem_success_status_info(){
    console.log(`calling show_checkin_redeem_status_info`)

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_checkin_redeem_success_result_info.title}</h5>
        <p class="bot_header">${botView.current_checkin_redeem_success_result_info.content}</p>
        `
    }   
}

function show_checkin_purchase_success_status_info(){
    console.log('calling show_checkin_purchase_success_status_info');

    const botInfoDisplay = document.getElementById('botInfoDisplay');

    if(botInfoDisplay){
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML=`
        <h5 class="bot_header">${botView.current_checkin_purchase_success_result_info.title}</h5>
        <p class="bot_header">${botView.current_checkin_purchase_success_result_info.content}</p>
        `
    }
}

function show_checkin_redeem_success_navigation(){
    console.log(`calling show_checkin_redeem_navigation`)

    const botNavigation = document.getElementById("botNavigation");

    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_checkin_redeem_success_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }
}

function show_checkin_purchase_success_navigation(){
    console.log(' calling show_checkin_purchase_success_navigation')

    const botNavigation = document.getElementById("botNavigation");
    
    if (botNavigation){
        botNavigation.style.display = "block";

        botView.current_checkin_purchase_success_buttons.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;

            botNavigation.appendChild(buttonBig);
        });


    }

}

function showCriticalConsoleError(data) {
    const botInfoDisplay = document.getElementById('botInfoDisplay');
    let callStack = "Unknown Call Stack";
    let errorLocation = "Unknown Location";

    // Parse the stack trace to identify the calling functions and location
    try {
        const stackLines = new Error().stack.split("\n");
        
        if (stackLines.length > 1) {
            // Extract error location from the first relevant stack line
            const errorLine = stackLines[2] || ""; // Line after this function call
            const locationMatch = errorLine.match(/\((.*?):(\d+):(\d+)\)/);

            if (locationMatch) {
                const [_, file, line, column] = locationMatch;
                errorLocation = `File: ${file}, Line: ${line}, Column: ${column}`;
            }

            // Format the stack trace
            callStack = stackLines.slice(1).map((line, index) => `#${index} ${line.trim()}`).join("<br>");
        }
    } catch (error) {
        console.error("Error retrieving call stack:", error);
        callStack = "Unable to retrieve call stack.";
    }

    // Display the error in the bot interface
    if (botInfoDisplay) {
        botInfoDisplay.style.display = "block";
        botInfoDisplay.innerHTML = `
            <h5 class="bot_header">Environment Error</h5>
            <p class="bot_header"><strong>Error Location:</strong> ${errorLocation}</p>
            <p class="bot_header"><strong>Call Stack:</strong></p>
            <p class="bot_header">${callStack}</p>
            <p class="bot_header"><strong>Error Details:</strong> ${data}</p>
        `;
    }
}

function show_game_boy_advance_items_of_sale(){
    console.log(`calling show_game_boy_advance_items_of_sale `)
    // check if itemCardContainer is active
    const itemCardContainer = document.getElementById('itemCardContainer');
    if(itemCardContainer){
        itemCardContainer.style.display="none"
    }

    const GBAItemCardContainer = document.getElementById('GBAItemCardContainer');
    if(GBAItemCardContainer){
        GBAItemCardContainer.style.display="block"
        GBAItemCardContainer.innerHTML=""
    }

    items_of_sale[1].forEach(item => {
        if (item.public) {
            const card = document.createElement('div');
            card.classList.add('item_card');
            card.innerHTML = `
                <img class="item_card_image" src="./static/media_store/${item.item_media_url}" alt="${item.title}">
                <div class="item_info">
                    <div class="item_info_title">
                        <h3 class="item_title">${item.title}</h3>
                        <p class="item_price">Ksh ${item.price}</p>
                    </div>
                    <p class="item_name">${item.name}</p>
                    <p class="item_description">${item.description}</p>
                </div>
                <form class="item_get_button_layer itemForm">
                    <input type="hidden" name="make_order_item_id" value="${item.id}">
                    <button class="item_get_button">Get</button>
                </form>
            `;
            GBAItemCardContainer.appendChild(card);
        }
    });

    
    
}



function show_game_boy_advance_display(){
    console.log('calling show_game_boy_advance_display')
    // document.getElementById('itemCardContainer').style.display= "none";
    document.getElementById('botScreenBig').src = botView.landing_game_screen_media[0]
}

function show_game_boy_advance_button_stack(){
    console.log('calling show_game_boy_advance_button_stack')
    fold_bot_start_display();
    show_game_landing_info();
    show_game_top_button_stack();

    // show_game_middle_button_stack();
    
    // show_game_gameboy_advance_button_stack();
    show_game_extra_button_stack();
}

function show_game_landing_info(){
    console.log('calling show_game_landing_info');

    let botHeader = document.getElementById("botHeader");

    botHeader.innerHTML = 'Game Boy Advance'
    botHeader.style.display = "block"
}

function show_game_top_button_stack(){
    console.log('calling show_game_top_button_stack');

    const botGBATopButtonStack = document.getElementById("botGBATopButtonStack");

    if (botGBATopButtonStack){
        botGBATopButtonStack.style.display = "block";

        const gba_top_button_stack_list = botView.landing_game_top_buttons;

        botGBATopButtonStack.innerHTML = ""

        gba_top_button_stack_list.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;
            botGBATopButtonStack.appendChild(buttonBig); // Fix the appendChild call
        });
    }   
    else{
        console.error("Element botGBATopButtonStack not found")
    }
}

function show_game_middle_button_stack() {
    console.log('calling show_game_middle_button_stack');

    const botGBAMiddleButtonStack = document.getElementById("botGBAMiddleButtonStack");

    if (botGBAMiddleButtonStack) {
        botGBAMiddleButtonStack.style.display = "block";

        const gba_middle_button_stack_list = botView.landing_game_middle_buttons; // Initialize an empty array or populate it with buttons

        // Clear existing content in the stack (optional, depends on your use case)
        botGBAMiddleButtonStack.innerHTML = ""

        gba_middle_button_stack_list.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;
            botGBAMiddleButtonStack.appendChild(buttonBig); // Fix the appendChild call
        });
    } else {
        console.error("Element 'botGBAMiddleButtonStack' not found");
    }
}

function show_game_gameboy_advance_button_stack(){
    console.log('calling show_game_gameboy_advance_button_stack')

    const botGBAPlayButtonStack = document.getElementById('botGBAPlayButtonStack');

    if(botGBAPlayButtonStack){
        botGBAPlayButtonStack.style.display = "block";

        const gba_game_play_button_stack_list = botView.landing_game_gba_buttons;

        botGBAPlayButtonStack.innerHTML = "";

        gba_game_play_button_stack_list.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;
            botGBAPlayButtonStack.appendChild(buttonBig); // Fix the appendChild call
        });
    }
    else{
        console.error('Element botGBAPlayButtonStack not found')
    }

}   

function show_game_extra_button_stack(){
    console.log('calling show_game_extra_button_stack');

    const botGBAFooterButtonStack = document.getElementById('botGBAFooterButtonStack');

    if(botGBAFooterButtonStack){

        botGBAFooterButtonStack.style.display = "block";

        const gba_game_footer_button_stack_list = botView.landing_game_extra_buttons;

        botGBAFooterButtonStack.innerHTML = "";

        gba_game_footer_button_stack_list.forEach(button => {
            const buttonBig = document.createElement('div');
            buttonBig.classList.add('bot_button_layer');
            buttonBig.innerHTML = `
                <input type="hidden" name="intent" value="${button.label}">
                <button class="bot_button" id="${button.id}" onclick="process_button_master(this)">
                    <div class="row">
                        <div class="col-8">
                            <span class="type-label">${button.label}</span>
                        </div>
                        <div class="col-4">
                            <span class="type_label"><i class="${button.icon}"></i></span>
                        </div>
                    </div>
                </button>
            `;
            botGBAFooterButtonStack.appendChild(buttonBig); // Fix the appendChild call
        });
    }
    else{
        console.error('Element botGBAPlayButtonStack not found')
    }
}



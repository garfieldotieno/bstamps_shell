
@tele_bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    # Retrieve the sticker file ID
    sticker_file_id = message.sticker.file_id
    
    # Log or print the sticker file ID for reference
    print(f"Received sticker with file ID: {sticker_file_id}")
    
    # Send a response message acknowledging the sticker
    tele_bot.send_message(message.chat.id, "Nice sticker! Thanks for sharing.")
    
    # Optionally, you can also send a sticker back to the user
    # Here, replace 'CAADAgADQAADyIsGAAE7MpzFPFQX7QI' with the file ID of the sticker you want to send
    response_sticker_file_id = sticker_file_id
    tele_bot.send_sticker(message.chat.id, response_sticker_file_id)


@app.route('/telegram', methods=['POST'])
def tele_webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            print(f"\n\nstep one : getting the contents from json input \n\n")

            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
        except Exception as e:
            print(f"error t step one : {e}") 

        # Process the update only once
        tele_bot.process_new_updates([update])
        
        if update.message:
            print(f"\n\nstep two : getting messge from update.messge object \n\n")
            try:

                user_id = update.message.from_user.id
                user_name = update.message.from_user.username
                client_input = update.message.text.lower() if update.message.text else ''

                # Print or process the extracted data
                print(f"User ID: {user_id}, Username: {user_name}, Client Input: {client_input}")
                db = SessionLocal()

            except Exception as e:
                print(f"error at step two : {e}")

            if Session.is_first_time_contact(user_id):
                print(f"\n\nstep three calling F_C \n\n")
                print(f"is continuing user")
                
                try:
                    
                    if Session.is_active(user_id):
                        print(f"and user is active")
                        return 'ok'
                    else:
                        print(f"user is not active")
                        if int(Session.is_main_menu_nav(user_id)) == 1:
                            print(f"\n\nis main menu navigation\n\n")


                            if client_input in ["browse", "select", "cancel"]:
                                if client_input == "cancel":
                                    print(f"\n\nmain menu input -- cancel\n\n")
                                    # cancel selected

                                    acc_type = Session.get_session_type(user_id)
                                    
                                    if acc_type == "First":
                                        Session.reset_browsing_count(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"current payload after reseting \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                        return 'ok'
                                    
                                    if acc_type == "Customer":
                                        Session.reset_browsing_count(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        menu_payload = main_menu_customer_session_listing[current_count]
                                        print(f"current payload after reseting \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                        return 'ok' 

                                    if acc_type == "Vendor":
                                        Session.reset_browsing_count(user_id)

                                        current_count = Session.get_browsing_count(user_id)
                                        menu_payload = main_menu_vendor_session_listing[current_count]
                                        print(f"current payload after reseting \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())
                                        return 'ok' 


                                     

                                if client_input == "select": 
                                    print(f"\n\nmain menu input -- select\n\n")

                                    acc_type = Session.get_session_type(user_id)
                                    current_count = Session.get_browsing_count(user_id)
                                    print(f"current count is : {current_count}")

                                    
                                    if acc_type == "First":
                                        main_menu_code = main_menu_no_session_listing[current_count]['menu_code']

                                        if main_menu_code in ['ACCOUNT', 'ABOUT'] :
                                            Session.reset_browsing_count(user_id)

                                            if main_menu_code == "ACCOUNT":
                                                Session.on_sub1_menu_nav(user_id, 'acc_sub1menu_listing')
                                                # Session.load_submenu(user_id, 'acc_submenu_listing')

                                                # load
                                                submenu_payload = authenticate_sub1_menu_listing[0]
                                                submenu_message = submenu_payload['menu_message']
                                                submenu_sticker = submenu_payload['menu_sticker']
                                                submenu_media = submenu_payload['media'][0]

                                                tele_bot.send_sticker(user_id, submenu_sticker)
                                                tele_bot.send_photo(user_id, submenu_media)
                                                tele_bot.send_message(user_id, submenu_message)
                                                return 'ok' 

                                            if main_menu_code == "ABOUT":
                                                Session.on_sub1_menu_nav(user_id, 'abt_sub1menu_listing')
                                                # Session.load_submenu(user_id, 'acc_submenu_listing')

                                                # load
                                                submenu_payload = abt_sub1_menu_listing[0]
                                                submenu_message = submenu_payload['menu_message']
                                                submenu_sticker = submenu_payload['menu_sticker']
                                                submenu_media = submenu_payload['media'][0]

                                                tele_bot.send_sticker(user_id, submenu_sticker)
                                                tele_bot.send_photo(user_id, submenu_media)
                                                tele_bot.send_message(user_id, submenu_message)
                                                return 'ok' 

                                             

                                    if acc_type == "Customer":
                                        pass 
                                    if acc_type == "Vendor":
                                        pass 

                                    return 'ok'

                                if client_input == "browse":
                                    print(f"\n\nmain menu input -- browse\n\n")
                                    
                                    acc_type = Session.get_session_type(user_id)

                                    if acc_type == "First":
                                        Session.browse_main(user_id, len(main_menu_no_session_listing))

                                        current_count = Session.get_browsing_count(user_id)

                                        print(f"check menu type, then load response, with browsing current_count being : {current_count}")
                                    

                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"First : current payload during main browsing \n\n {menu_payload}")

                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_session_menu_code(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok' 

                                    if acc_type == "Customer":
                                        Session.browse_main(user_id, len(main_menu_no_session_listing))

                                        current_count = Session.get_browsing_count(user_id)

                                        print(f"check menu type, then load response, with browsing current_count being : {current_count}")
                                    
                                        menu_payload = main_menu_no_session_listing[current_count]
                                        print(f"Customer : current payload during main browsing \n\n {menu_payload}")

                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_session_menu_code(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok' 

                                    if acc_type == "Vendor":
                                        menu_payload = main_menu_vendor_session_listing[current_count]
                                        print(f"Vendor : current payload during main browsing \n\n {menu_payload}")
                                        # Send the message with buttons and media

                                        menu_code = menu_payload['menu_code']
                                        Session.update_session_menu_code(user_id, menu_code)

                                        tele_bot.send_chat_action(update.message.chat.id, 'typing')
                                        sticker_file_id = menu_payload['menu_sticker']
                                        image_link = menu_payload['media'][0]

                                        tele_bot.send_sticker(update.message.chat.id, sticker_file_id)
                                        tele_bot.send_photo(update.message.chat.id, image_link)
                                        tele_bot.send_message(user_id, f"{menu_payload['menu_message']}", reply_markup=main_markup())

                                        return 'ok'
                                
                                         

                                    
                                    
                        else :
                            print(f"could be sub_menu[1,2] or slot filling")
                            return 'ok'
                
                    
                except Exception as e:
                    print(f"error at step three : {e}")
            else:
                print(f"\n\nstep four : calling A\n\n")
                try:
                        
                    print(f"is user first time, creating session")

                    new_count = 0

                    if client_input:
                        print(f"\n\nstep five, creating user session \n\n")

                        try:


                            print(f"starting to process first input, /start")

                            new_user_session = Session(
                            uid=generate_uid(),
                            waid=user_id,
                            name=user_name,

                            current_menu_code='ACC',
                            browsing_count=new_count,

                            main_menu_nav=1,
                            main_menu_select='',
                            sub1_menu_nav=0,
                            sub1_menu_select='',
                            sub2_menu_nav=0,
                            sub2_menu_select='',

                            is_slot_filling=0,
                            answer_payload='[]',
                            
                            user_flow='',
                            current_slot_code='',
                            current_slot_count=0,
                            slot_quiz_count='',

                            current_slot_handler='',
                            session_active=0,
                            session_type='First'
                            )

                            new_user_session.save() 
                            # ommitting account summary
                            current_count = Session.get_browsing_count(user_id)

                            menu_payload = main_menu_no_session_listing[current_count]
                            print(f"current menu payload : {menu_payload}")

                            menu_message = menu_payload['menu_message']
                            menu_code = menu_payload['menu_code']

                            Session.update_session_menu_code(user_id, menu_code)

                            tele_bot.send_chat_action(update.message.chat.id, 'typing')
                            sticker_file_id = menu_payload['menu_sticker']
                            image_link = menu_payload['media'][0]

                            tele_bot.send_sticker(update.message.chat.id, sticker_file_id)

                            tele_bot.send_photo(update.message.chat.id, image_link)

                            tele_bot.send_message(user_id, menu_message, reply_markup=main_markup())

                            return 'ok'
                        
                        except Exception as e:
                            print(f"error at step five : {e}")
                
                except Exception as e:
                    print(f"error at step four : {e}")
        
        
        else:
            return 'ok'

                
    else:
        return 'invalid request', 403

if __name__ == '__main__':
    with app.app_context():
        # time.sleep(0.5)
        tele_bot.set_webhook(url="https://c63c-2c0f-2a80-10c8-4f10-a75d-4ae-e94a-e677.ngrok-free.app/telegram")

    app.run(debug=True, port=PORT)
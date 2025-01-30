# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"
import json
import os.path
import os
import random
import smtplib
import traceback
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk import FormValidationAction
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import FollowupAction, ActiveLoop


def send_email(development_type: str, platform: str, category: str, desc: str, name: str, email: str):
    try:
        message_data = EmailMessage()
        message_data["Subject"] = "New Mobile App Development Inquiry"
        username = 'digi-bot'
        password = 'KdccnPbfkHG0DwTE'
        message_data["From"] = "support@digimonksolutions.com"
        message_data["To"] = email

        email_body = f'''
            <html>
            <head>
                <style>
                    h2 {{
                        color: #333;
                        font-size: 24px;
                        margin-bottom: 10px;
                    }}
                    p {{
                        color: #555;
                        font-size: 16px;
                        margin-bottom: 20px;
                    }}
                </style>
            </head>
            <body>
                <h2>User Details</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <h2>Email Details</h2>
                <p><strong>Development Type:</strong> Mobile Development </p>
                <p><strong>Mobile Development Type:</strong> {development_type}</p>
                <p><strong>{development_type} Platform:</strong> {platform}</p>
                <p><strong>App Category:</strong> {category}</p>
                <h2>App Description</h2>
                <p>{desc}</p>
            </body>
            </html>
            '''

        message_data.add_alternative(email_body, subtype='html')

        with smtplib.SMTP_SSL("mail.smtp2go.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(message_data)
            smtp_server.quit()
        return True
    except Exception as error:
        logger.error(f"Error: {error}")
        logger.info(traceback.print_exc())
        return False


class ActionSaveConversation(Action):

    def name(self) -> Text:
        return "action_save_conversation"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        conversation = tracker.events
        print(conversation)
        if not os.path.isfile('chats' + str(tracker.sender_id) + '.csv'):
            with open('chats' + str(tracker.sender_id) + '.csv', 'w', encoding="utf-8") as file:
                file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")
                file.close()
        chat_data = ''
        for i in conversation:
            if i['event'] == 'user':
                chat_data += i['parse_data']['intent']['name'] + ',' + i['text'] + ','
                print('user: {}'.format(i['text']))
                if len(i['parse_data']['entities']) > 0:
                    chat_data += i['parse_data']['entities'][0]['entity'] + ',' + i['parse_data']['entities'][0][
                        'value'] + ','
                    print('extra data:', i['parse_data']['entities'][0]['entity'], '=',
                          i['parse_data']['entities'][0]['value'])
                else:
                    chat_data += ",,"
            elif i['event'] == 'bot':
                print('Bot: {}'.format(i['text']))
                try:
                    chat_data += i['metadata']['utter_action'] + ',' + i['text'] + '\n'
                except KeyError:
                    pass
        else:
            with open('chats' + str(tracker.sender_id) + '.csv', 'a', encoding="utf-8") as file:
                file.write(str(chat_data))
                file.close()
        try:
            # Create a multipart message
            msg = MIMEMultipart()
            body_part = MIMEText("Conversation of sender id:- " + str(tracker.sender_id), 'plain')
            msg['Subject'] = "Conversation of sender id:- " + str(tracker.sender_id)
            msg['From'] = "support@digimonksolutions.com"
            msg['To'] = "karan.t@digimonksolutions.com"
            username = 'digi-bot'
            password = 'KdccnPbfkHG0DwTE'
            # Add body to email
            msg.attach(body_part)
            # open and read the CSV file in binary
            with open('chats' + str(tracker.sender_id) + '.csv', 'rb') as file:
                # Attach the file with filename to the email
                msg.attach(MIMEApplication(file.read(), Name="CSV_" + str(tracker.sender_id) + ".csv"))
            # Create SMTP object
            with smtplib.SMTP_SSL("mail.smtp2go.com", 465) as smtp_server:
                smtp_server.login(username, password)
                smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
                smtp_server.quit()
                os.remove(file.name)
        except Exception as error:
            logger.error(f"Error: {error}")
            logger.info(traceback.print_exc())

        return []


class ActionMobileAppDevelopment(Action):
    def name(self) -> Text:
        return "action_mobile_development"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Native app development ",
                        "subtitle": "Native app development is the process of creating an app that is specifically designed for a particular operating system, such as iOS or Android. Native apps are typically written in the native programming language for the target platform, such as Swift for iOS or Java for Android. This allows native apps to take full advantage of the features and capabilities of the underlying operating system, resulting in faster performance, better user experience, and more access to native platform APIs. ",
                        "image_url": "https://www.mindinventory.com/blog/wp-content/uploads/2022/10/native-app-development-1024x512.png",
                        "buttons": [
                            {
                                "title": "👉 Go with Native",
                                "payload": "/native_app_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Cross-platform app development",
                        "subtitle": "Cross-platform app development is the process of creating an app that can be "
                                    "used on multiple operating systems, such as iOS, Android, and Windows. "
                                    "Cross-platform apps are typically written in a language that can be compiled for "
                                    "multiple platforms, such as JavaScript or Kotlin. This allows cross-platform "
                                    "apps to be developed more quickly and easily than native apps, but they may not "
                                    "offer the same level of performance or user experience. ",
                        "image_url": "https://www.netsolutions.com/insights/wp-content/uploads/2020/12/Cross-Platform"
                                     "-App-Development.jpg.webp",
                        "buttons": [
                            {
                                "title": "👉 Go with Cross-platform",
                                "payload": "/cross_platform_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionNativeAppDevelopmentCarousel(Action):
    def name(self) -> Text:
        return "action_native_app_development"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "IOS",
                        "subtitle": "IOS development offers a robust and comprehensive platform for building native "
                                    "applications specifically for Apple devices. It provides a rich set of tools, "
                                    "frameworks, and resources to create high-quality apps that take advantage of the "
                                    "unique features of iOS devices.",
                        "image_url": "https://developer.apple.com/news/images/og/ios-17-og.jpg",
                        "buttons": []
                    },
                    {
                        "title": "Android",
                        "subtitle": "Android development offers a versatile and open platform for creating native "
                                    "applications that can run on a wide range of devices. It provides powerful "
                                    "tools, extensive APIs, and a global distribution platform, making it an "
                                    "attractive choice for developers aiming to reach a broad audience.",
                        "image_url": "https://lh3.googleusercontent.com/GTmuiIZrppouc6hhdWiocybtRx1Tpbl52eYw4l"
                                     "-nAqHtHd4BpSMEqe-vGv7ZFiaHhG_l4v2m5Fdhapxw9aFLf28ErztHEv5WYIz5fA",
                        "buttons": []
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return [SlotSet("development_type", "Native")]


class ActionCrossPlatformAppDevelopmentCarousel(Action):
    def name(self) -> Text:
        return "action_cross_platform_app_development"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Flutter",
                        "subtitle": "Flutter provides a streamlined and efficient approach to mobile app development, "
                                    "empowering developers to create visually appealing, high-performance "
                                    "applications across multiple platforms with ease.",
                        "image_url": "https://storage.googleapis.com/cms-storage-bucket/70760bf1e88b184bb1bc.png",
                        "buttons": [
                            {
                                "title": "👉 Go with Flutter",
                                "payload": "/flutter_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "React Native",
                        "subtitle": "React Native is a JavaScript framework developed by Meta (formerly Facebook). It "
                                    "is used to create native-looking mobile apps using React, a popular JavaScript "
                                    "library for building user interfaces. React Native is known for its ability to "
                                    "leverage native components, which can improve performance and user experience. ",
                        "image_url": "https://www.metaltoad.com/sites/default/files/styles"
                                     "/large_personal_photo_870x500_/public/2020-05/react-js-blog-header.png?itok"
                                     "=VbfDeSgJ",
                        "buttons": [
                            {
                                "title": "👉 Go with React",
                                "payload": "/react_native_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },

                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return [SlotSet("development_type", "Cross Platform")]


class ActionSetSlotForNativeDevelopmentType(Action):

    def name(self) -> Text:
        return "action_set_slot_native_development_type"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        last_message_intent = tracker.get_intent_of_latest_message()

        # dispatcher.utter_message(response="utter_select_app_category_desc")
        if last_message_intent == "android_development":
            return [SlotSet("native_development_type", "Android")]
        elif last_message_intent == "ios_development":
            return [SlotSet("native_development_type", "IOS")]
        else:
            return [SlotSet("native_development_type", "Both Android & IOS")]


class ActionSetSlotForWebDevelopmentTech(Action):

    def name(self) -> Text:
        return "action_set_slot_web_development_tech"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        last_message_intent = tracker.get_intent_of_latest_message()

        # dispatcher.utter_message(response="utter_select_app_category_desc")
        if last_message_intent == "wordpress_development":
            return [SlotSet("web_development_tech", "Wordpress Development")]
        elif last_message_intent == "react_js_development":
            return [SlotSet("web_development_tech", "React JS Development")]
        else:
            return [SlotSet("web_development_tech", "")]


class ActionSetSlotForCrossPlatformType(Action):

    def name(self) -> Text:
        return "action_set_slot_cross_platform_development_type"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        last_message_intent = tracker.get_intent_of_latest_message()

        # dispatcher.utter_message(response="utter_select_app_category_desc")
        if last_message_intent == "flutter_development":
            return [SlotSet("cross_platform_development_type", "Flutter")]
        elif last_message_intent == "react_native_development":
            return [SlotSet("cross_platform_development_type", "React Native")]
        else:
            return [SlotSet("cross_platform_development_type", "")]


class ActionSetSlotsForHiringDeveloper(Action):
    def name(self) -> Text:
        return "action_set_slot_for_hiring_developer"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        slot_list = []
        if tracker.slots.get("hiring_development_type") is not None:
            slot_list.append(SlotSet("hiring_development_type_value", tracker.slots.get("hiring_development_type")))
            if "mobile" not in str(tracker.slots.get("hiring_development_type")).lower():
                slot_list.append(SlotSet("hiring_mobile_platform_value", "None"))

        if tracker.slots.get("hiring_tech_type") is not None:
            slot_list.append(SlotSet("hiring_tech_type_value", tracker.slots.get("hiring_tech_type")))

        if tracker.slots.get("hiring_project_timeline") is not None:
            slot_list.append(SlotSet("hiring_project_timeline_value", tracker.slots.get("hiring_project_timeline")))

        if tracker.slots.get("hiring_mobile_platform") is not None:
            slot_list.append(SlotSet("hiring_mobile_platform_value", tracker.slots.get("hiring_mobile_platform")))
            slot_list.append(SlotSet("hiring_development_type_value", "Mobile"))

        return slot_list


class ValidateHiringDevelopersForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_hiring_developer_form"

    def validate_hiring_email_value(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent_of_last_user_message = tracker.get_intent_of_latest_message()
        print(tracker.get_slot("email"))
        if intent_of_last_user_message != "provided_email":
            dispatcher.utter_message("That must've been a typo.")
            return {"hiring_email_value": None}

        return {"hiring_email_value": tracker.get_slot("email")}

    def validate_hiring_development_type_value(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if "mobile" not in str(tracker.slots.get("hiring_development_type")).lower():
            return {"hiring_mobile_platform_value": "None"}

        return {}


class ValidateNativeDevelopmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_native_development_form"

    def validate_email_for_app_dev(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent_of_last_user_message = tracker.get_intent_of_latest_message()
        print(tracker.get_slot("email"))
        if intent_of_last_user_message != "provided_email":
            dispatcher.utter_message("That must've been a typo.")
            return {"email_for_app_dev": None}

        return {"email_for_app_dev": tracker.get_slot("email")}


class ValidateWebDevelopmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_web_development_form"

    def validate_email_for_web_dev(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent_of_last_user_message = tracker.get_intent_of_latest_message()
        print(tracker.get_slot("email"))
        if intent_of_last_user_message != "provided_email":
            dispatcher.utter_message("That must've been a typo.")
            return {"email_for_web_dev": None}

        return {"email_for_web_dev": tracker.get_slot("email")}


class ValidateWebApplicationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_web_app_form"

    def validate_email_for_web_app(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent_of_last_user_message = tracker.get_intent_of_latest_message()
        print(tracker.get_slot("email"))
        if intent_of_last_user_message != "provided_email":
            dispatcher.utter_message("That must've been a typo.")
            return {"email_for_web_app": None}

        return {"email_for_web_app": tracker.get_slot("email")}


class ValidateWebsiteUpdateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_website_update_form"

    def validate_website_update_user_email(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent_of_last_user_message = tracker.get_intent_of_latest_message()
        print(tracker.get_slot("email"))
        if intent_of_last_user_message != "provided_email":
            dispatcher.utter_message("That must've been a typo.")
            return {"website_update_user_email": None}

        return {"website_update_user_email": tracker.get_slot("email")}


class ActionSendDetails(Action):
    def name(self) -> Text:
        return "action_send_details"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        development_type = tracker.get_slot('development_type')
        platform = tracker.get_slot('native_development_type') + tracker.get_slot('cross_platform_development_type')
        category = tracker.get_slot('app_category')
        description = tracker.get_slot('app_description')
        name = tracker.get_slot('name_for_app_dev')
        email = tracker.get_slot('email_for_app_dev')

        send_email(development_type, platform, category, description, name, email)
        return []


class ActionShowWebsiteDevelopmentTechnologiesList(Action):
    def name(self) -> Text:
        return "action_show_website_tech_list"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Wordpress Development",
                        "subtitle": "WordPress is the most popular content management system (CMS) in the world. It's easy to use, customizable, and SEO-friendly. With WordPress, you can create a website that looks great and is easy to manage.",
                        "image_url": "https://s.w.org/style/images/about/WordPress-logotype-alternative.png",
                        "buttons": [
                            {
                                "title": "👉 Go with Wordpress",
                                "payload": "/wordpress_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "React JS Development",
                        "subtitle": "React JS is a JavaScript library for building user interfaces. It's declarative, "
                                    "efficient, and flexible. With React JS, you can create dynamic user interfaces "
                                    "that are easy to use and maintain.",
                        "image_url": "https://bitnetinfotech.com/wp-content/uploads/2022/08/Frameworks-for-React-JS.jpg",
                        "buttons": [
                            {
                                "title": "👉 Go with React JS",
                                "payload": "/react_js_development",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },

                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return [SlotSet("web_development_type", "Website")]


class ActionShowBackendTechnologies(Action):
    def name(self) -> Text:
        return "action_show_backend_tech_list"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": ".NET",
                        "subtitle": ".NET is a free, cross-platform, open-source developer platform that can be used "
                                    "to build many different types of applications. It is developed by Microsoft and "
                                    "uses the C# programming language.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Microsoft_.NET_logo"
                                     ".svg/456px-Microsoft_.NET_logo.svg.png?20200524040737",
                        "buttons": [
                            {
                                "title": "👉 Go with .NET",
                                "payload": "ASP.NET",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "PHP",
                        "subtitle": "PHP is a server-side scripting language that is used to create dynamic web "
                                    "pages. It is one of the most popular programming languages in the world, "
                                    "and is used by over 80% of websites.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/PHP-logo.svg/711px"
                                     "-PHP-logo.svg.png?20180502235434",
                        "buttons": [
                            {
                                "title": "👉 Go with PHP",
                                "payload": "PHP",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Laravel",
                        "subtitle": "Laravel is a free, open-source PHP framework that is used to develop web "
                                    "applications. It is known for its elegant syntax, powerful features, "
                                    "and large community.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Laravel.svg/1024px"
                                     "-Laravel.svg.png",
                        "buttons": [
                            {
                                "title": "👉 Go with Laravel",
                                "payload": "Laravel",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Node.js",
                        "subtitle": "Node.js is an open-source, cross-platform runtime environment that allows "
                                    "JavaScript to be used outside of a web browser. It is used to build real-time "
                                    "applications, web servers, and command-line tools.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Node.js_logo.svg",
                        "buttons": [
                            {
                                "title": "👉 Go with Node.js",
                                "payload": "Node.js",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return [SlotSet("web_development_type", "Web Application")]


class ActionSetBackendTechNotSure(Action):
    def name(self) -> Text:
        return "action_set_backend_tech_not_sure"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("backend_tech_web_app", "Not Sure")]


class ActionShowFrontendTechnologies(Action):
    def name(self) -> Text:
        return "action_show_frontend_tech_list"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "React JS",
                        "subtitle": "A JavaScript library that is used to build user interfaces. It is a declarative "
                                    "library, which means that you describe how the UI should look and behave, "
                                    "and React takes care of the underlying code needed to make that happen. React is "
                                    "used by many popular websites and applications, such as Facebook, Instagram, "
                                    "and Netflix.",
                        "image_url": "https://bitnetinfotech.com/wp-content/uploads/2022/08/Frameworks-for-React-JS.jpg",
                        "buttons": [
                            {
                                "title": "👉 Go with React JS",
                                "payload": "go with react.js",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                    {
                        "title": "Angular JS",
                        "subtitle": "A JavaScript framework that is also used to build user interfaces. It is a more "
                                    "comprehensive framework than React JS, and it provides more features and "
                                    "functionality. Angular JS is used by many popular websites and applications, "
                                    "such as YouTube, Google Maps, and Gmail.",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/AngularJS_logo.svg"
                                     "/1920px-AngularJS_logo.svg.png",
                        "buttons": [
                            {
                                "title": "👉 Go with Angular JS",
                                "payload": "Angular",
                                "type": "postback"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    },
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return [SlotSet("web_development_type", "Web Application")]


class ActionSetFrontendTechNotSure(Action):
    def name(self) -> Text:
        return "action_set_frontend_tech_not_sure"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("frontend_tech_web_app", "Not Sure")]


class ActionShowPortfolio(Action):
    def name(self) -> Text:
        return "action_show_portfolio"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        with open(os.path.curdir + "/actions/data/portfolio_data.json", "r", encoding="utf-8") as file:
            additional_elements = json.load(file)

        elements = []
        # Randomly select a subset of elements from the combined list
        num_random_elements = 5  # Adjust this value as needed
        random_elements = random.sample(additional_elements, num_random_elements)
        elements.extend(random_elements)
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowBlogs(Action):
    def name(self) -> Text:
        return "action_show_blogs"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        with open(os.path.curdir + "/actions/data/blogs_data.json", "r", encoding="utf-8") as file:
            additional_elements = json.load(file)

        elements = []
        # Randomly select a subset of elements from the combined list
        num_random_elements = 5  # Adjust this value as needed
        random_elements = random.sample(additional_elements, num_random_elements)
        elements.extend(random_elements)
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowAppDevelopmentCost(Action):
    def name(self) -> Text:
        return "action_show_app_development_cost"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "How much does it cost to develop an App in 2023?",
                        "subtitle": "When developing an app, whether for business requirements or to kickstart a side hustle, the first thing that strikes the mind is the cost of",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/02/Blog-Image-01-min-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/app-development-cost/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowAndroidAppDevelopmentCost(Action):
    def name(self) -> Text:
        return "action_show_android_app_development_cost"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "How much does Android App Development Costs in 2023?",
                        "subtitle": "Mapping Out Your Android App Development Budget: How to Accurately Estimate Android App Development Costs in 2023.",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/09/01-Featured-Image-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/android-app-development-cost/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowIOSAppDevelopmentCost(Action):
    def name(self) -> Text:
        return "action_show_ios_app_development_cost"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "How much does iOS App Development Costs in 2023?",
                        "subtitle": "Get a complete guide to iOS app development costs, including factors that affect price and tips on how to save money.",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/10/iOS-App-Development-Cost-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/ios-app-development-costs/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowWebsiteDevelopmentCost(Action):
    def name(self) -> Text:
        return "action_show_website_development_cost"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "How much does it cost to develop a Website in 2023​?",
                        "subtitle": "Right from the beginning of the 21st century, there have been tremendous advancements in the IT industry, attracting everyone to the world of the internet.",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/02/Website-development-cost-scaled.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/website-development-cost/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowNativeVSCrossPlatform(Action):
    def name(self) -> Text:
        return "action_show_native_vs_cross_platform"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Native Vs Cross Platform: Which is Best For Your App in 2023?",
                        "subtitle": "Native or Cross Platform: Which suits your app better in 2023? Get all the details you need to make an informed decision.",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/05/native-vs-cross-platform-1-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/native-vs-cross-platform/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowFlutterVSReactNative(Action):
    def name(self) -> Text:
        return "action_show_flutter_vs_react_native"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Flutter Vs React Native: Which is the best for 2023?",
                        "subtitle": "Confused between Flutter vs React Native? Checkout our article to figure out which is the best for your app development project.",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2019/06/flutter-vs-react-native-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/flutter-vs-react-native/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionShowWordpressVSShopify(Action):
    def name(self) -> Text:
        return "action_show_wordpress_vs_shopify"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        message = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "WordPress Vs Shopify: Choosing the Best for Your Online Store in 2023",
                        "subtitle": "When it comes to building an online store, selecting the right platform is crucial for your business's success. WordPress and Shopify are two popular platforms",
                        "image_url": "https://digimonksolutions.com/wp-content/uploads/2023/04/wordpress-vs-shopify-1024x576.jpg",
                        "buttons": [
                            {
                                "title": "❤️ Read more",
                                "url": "https://digimonksolutions.com/wordpress-vs-shopify/",
                                "type": "web_url"
                            },
                            {
                                "title": "👈 Go to Main Menu",
                                "payload": "/main_menu",
                                "type": "postback"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionResetAllSlots(Action):
    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(
            self,
            dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("app_description", None), SlotSet("name_for_app_dev", None), SlotSet("email_for_app_dev", None),
                FollowupAction("native_development_form"), ActiveLoop("native_development_form")]

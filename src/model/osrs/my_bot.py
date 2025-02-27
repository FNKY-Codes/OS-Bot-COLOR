import time

import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from utilities.api.morg_http_client import MorgHTTPSocket
import utilities.imagesearch as imsearch

class OSRSMyBot(OSRSBot):
    def __init__(self):
        bot_title = "Tutorial"
        description = "Basic Bot"
        super().__init__(bot_title=bot_title, description=description)
        # Set option variables below (initial value is only used during UI-less testing)
        self.running_time = 1
        self.take_breaks = True

    def create_options(self):
        """
        Use the OptionsBuilder to define the options for the bot. For each function call below,
        we define the type of option we want to create, its key, a label for the option that the user will
        see, and the possible values the user can select. The key is used in the save_options function to
        unpack the dictionary of options after the user has selected them.
        """
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_dropdown_option("take_breaks", "Take breaks?", ["Yes", "No"])

    def save_options(self, options: dict):
        """
        For each option in the dictionary, if it is an expected option, save the value as a property of the bot.
        If any unexpected options are found, log a warning. If an option is missing, set the options_set flag to
        False.
        """
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] == "Yes"
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg("Options set successfully.")
        self.options_set = True


    def main_loop(self):
        """
        When implementing this function, you have the following responsibilities:
        1. If you need to halt the bot from within this function, call `self.stop()`. You'll want to do this
           when the bot has made a mistake, gets stuck, or a condition is met that requires the bot to stop.
        2. Frequently call self.update_progress() and self.log_msg() to send information to the UI.
        3. At the end of the main loop, make sure to set the status to STOPPED.

        Additional notes:
        Make use of Bot/RuneLiteBot member functions. There are many functions to simplify various actions.
        Visit the Wiki for more.
        """
        # Setup APIs
        api_m = MorgHTTPSocket()

        tinderbox_img = imsearch.BOT_IMAGES.joinpath("items", "tinderbox.png")

        # Main loop
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:

            # 5% chance to take a break between clicks
            if rd.random_chance(probability=0.05) and self.take_breaks:
                self.take_break(max_seconds=15)
            
            
            if api_m.get_is_player_idle():
                if chicken := self.get_furthest_tag(clr.CYAN):
                    self.mouse.move_to(chicken.random_point())
                    if not self.mouseover_text(contains="Attack"):
                        self.log_msg("Moving Camera")
                        self.move_camera(rd.fancy_normal_sample(-90,90),0)
                        continue
                    self.log_msg("Target Found")
                    self.mouse.click()
            
            if chicken := self.get_furthest_tag(clr.CYAN):
                    self.mouse.move_to(chicken.random_point())
                    if not self.mouseover_text(contains="Attack"):
                        continue
            
            
            self.update_progress((time.time() - start_time) / end_time)

        self.update_progress(1)
        self.log_msg("Finished.")
        self.stop()
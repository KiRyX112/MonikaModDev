default persistent._mas_current_consumable = {
    0: {
        "prep_time": None,
        "consume_time": None,
        "id": None,
    },
    1: {
        "prep_time": None,
        "consume_time": None,
        "id": None
    }
}










default persistent._mas_consumable_map = dict()

init python in mas_consumables:

    TYPE_DRINK = 0
    TYPE_FOOD = 1


    CONTAINER_NONE = None
    CONTAINER_PLATE = "plate"
    CONTAINER_CUP = "cup"




    PROP_CONTAINER = "container"


    PROP_OBJ_REF = "obj_ref"


    PROP_PLUR = "plural"


    DLG_PREP_HOT_DRINK = {
        PROP_CONTAINER: CONTAINER_CUP,
        PROP_PLUR: False
    }

    DLG_NON_PREP_PASTRY = {
        PROP_CONTAINER: CONTAINER_NONE,
        PROP_PLUR: False
    }

    DLG_NON_PREP_CAKE = {
        PROP_CONTAINER: CONTAINER_PLATE,
        PROP_OBJ_REF: "slice",
        PROP_PLUR: False
    }






    consumable_map = dict()





init 5 python:
    import random

    class MASConsumable():
        """
        Consumable class

        PROPERTIES:
            consumable_id - id of the consumable
            consumable_type - Type of consumable this is
            disp_name - friendly name for this consumable
            dlg_props - dialogue properties for flows for this consumable
            start_end_tuple_list - list of (start_hour, end_hour) tuples
            acs - MASAccessory to display for the consumable
            split_list - list of split hours
            portable - NOTE: Only for drinks, whether or not Monika can take this with her when taking her somewhere
            should_restock_warn - whether or not Monika should warn the player that she's running out of this consumable
            late_entry_list - list of integers storing the hour which would be considered a late entry
            max_re_serve - amount of times Monika can get a re-serving of this consumable
            cons_chance - likelihood of Monika to keep having this consumable
            prep_low - bottom bracket of preparation time (NOTE: Should be passed in as number of seconds)
            prep_high - top bracket of preparation time (NOTE: Should be passed in as number of seconds)
            cons_low - bottom bracket of consumable time (NOTE: Should be passed in as number of seconds)
            cons_high - top bracket of consumable time (NOTE: Should be passed in as number of seconds)
            done_cons_until - the time until Monika can randomly have this consumable again
            get_cons_evl - evl to use for getting the consumable (no prep)
            finish_prep_evl - evl to use when finished preparing a consumable
            finish_cons_evl - evl to use when finished having a consumable
        """
        
        
        
        BREW_FINISH_EVL = "mas_finished_brewing"
        DRINK_FINISH_EVL = "mas_finished_drinking"
        DRINK_GET_EVL = "mas_get_drink"
        
        
        PREP_FINISH_EVL = "mas_finished_prepping"
        FOOD_FINISH_EVL = "mas_finished_eating"
        FOOD_GET_EVL = "mas_get_food"
        
        DEF_DONE_CONS_TD = datetime.timedelta(hours=2)
        
        LOW_STOCK_AMT = 10
        LOW_CRITICAL_STOCK_AMT = 1
        
        def __init__(
            self,
            consumable_id,
            consumable_type,
            disp_name,
            start_end_tuple_list,
            acs,
            split_list,
            dlg_props=None,
            portable=False,
            should_restock_warn=True,
            late_entry_list=None,
            max_re_serve=None,
            max_stock_amount=150,
            cons_chance=80,
            cons_low=10*60,
            cons_high=2*3600,
            prep_low=2*60,
            prep_high=4*60,
            get_cons_evl=None,
            finish_prep_evl=None,
            finish_cons_evl=None
        ):
            """
            MASConsumable constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                consumable_type - type of consumable:
                    0 - Drink
                    1 - Food

                disp_name - Friendly diaply name (for use in dialogue)

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)
                    NOTE: Does NOT support midnight crossover times. If needed, requires a separate entry
                    NOTE: end_hour is exclusive

                acs - MASAccessory object for this consumable

                split_list - list of split hours for prepping

                dlg_props - dialogue properties for use in generic labels. If None, an empty dict is used, and fallback text will be shown
                    AVAILABLE PROPERTIES:
                        - mas_consumables.PROP_CONTAINER - Container for this consumable
                        - mas_consumables.PROP_OBJ_REF - Object reference for this consumable (use if container is not applicable)
                        - mas_consumables.PROP_PLUR - Whether or not this should be referenced as plural in text

                    (Default: None)

                portable - NOTE: for drinks only. True if Monika can take this with her when going out
                    (Default: False)

                should_restock_warn - should Monika warn the player that this needs to be restocked?
                    (Default: True)

                late_entry_list - list of times storing when we should load in with a consumable already out
                    If None, the start times from the start_end_tuple_list are assumed
                    NOTE: must be the same length as start_end_tuple_list
                    (Default: None)

                max_re_serve - amount of times Monika can get a refill of this consumable
                    (Default: None)

                max_stock_amount - maximum amount of this consumable we can stock
                    (Default: 150)

                cons_chance - chance for Monika to continue having this consumable
                    (Default: 80/100)

                cons_low - low bracket for Monika to have this consumable
                    (NOTE: Should be passed in as seconds)
                    (Default: 10 minutes)

                cons_high - high bracket for Monika to have this consumable
                    (NOTE: Should be passed in as seconds)
                    (Default: 2 hours)

                prep_low - low bracket for prep time
                    (NOTE: Should be passed in as seconds)
                    (Default: 2 minutes)
                    NOTE: If set to None, this will not be considered preppable

                prep_high - high bracket for prep time
                    (NOTE: Should be passed in as seconds)
                    (Default: 4 minutes)
                    NOTE: If set to None, this will not be considered preppable

                get_cons_evl - evl to use for getting the consumable. If None, a generic is assumed
                    (Default: None)
                    NOTE: Should have an Event object associated with the label

                finish_prep_evl - evl to use when finished prepping. If None, a generic is assumed
                    (Default: None)
                    NOTE: Should have an Event object associated with the label

                finish_cons_evl - evl to use when finished consuming. If None, a generic is assumed
                    (Default: None)
                    NOTE: Should have an Event object associated with the label
            """
            if (
                consumable_type in store.mas_consumables.consumable_map
                and consumable_id in store.mas_consumables.consumable_map[consumable_type]
            ):
                raise Exception("consumable {0} already exists.".format(consumable_id))
            
            self.consumable_id=consumable_id
            self.consumable_type=consumable_type
            self.disp_name=disp_name
            self.start_end_tuple_list=start_end_tuple_list
            self.acs=acs
            self.portable=portable
            self.cons_chance=cons_chance
            self.cons_low=cons_low
            self.cons_high=cons_high
            
            if late_entry_list is None:
                self.late_entry_list=[]
                
                for start, end in start_end_tuple_list:
                    self.late_entry_list.append(start)
            else:
                self.late_entry_list=late_entry_list
            
            self.max_re_serve=max_re_serve
            self.max_stock_amount=max_stock_amount
            self.re_serves_had=0
            
            self.dlg_props = dlg_props if dlg_props else dict()
            self.split_list=split_list
            self.should_restock_warn=should_restock_warn
            self.prep_low=prep_low
            self.prep_high=prep_high
            
            
            if consumable_type == 0:
                self.get_cons_evl = get_cons_evl if get_cons_evl is not None else MASConsumable.DRINK_GET_EVL
                self.finish_prep_evl = finish_prep_evl if finish_prep_evl is not None else MASConsumable.BREW_FINISH_EVL
                self.finish_cons_evl = finish_cons_evl if finish_cons_evl is not None else MASConsumable.DRINK_FINISH_EVL
            else:
                self.get_cons_evl = get_cons_evl if get_cons_evl is not None else MASConsumable.FOOD_GET_EVL
                self.finish_prep_evl = finish_prep_evl if finish_prep_evl is not None else MASConsumable.PREP_FINISH_EVL
                self.finish_cons_evl = finish_cons_evl if finish_cons_evl is not None else MASConsumable.FOOD_FINISH_EVL
            
            
            self.done_cons_until=None
            
            
            if consumable_type not in store.mas_consumables.consumable_map:
                store.mas_consumables.consumable_map[consumable_type] = dict()
            
            store.mas_consumables.consumable_map[consumable_type][consumable_id] = self
            
            
            if consumable_id not in persistent._mas_consumable_map:
                persistent._mas_consumable_map[consumable_id] = {
                    "enabled": False,
                    "times_had": 0,
                    "servings_left": 0,
                    "has_restock_warned": False
                }
        
        def enabled(self):
            """
            Checks if this consumable is enabled

            OUT:
                boolean:
                    - True if this consumable is enabled
                    - False otherwise
            """
            return persistent._mas_consumable_map[self.consumable_id]["enabled"]
        
        def enable(self):
            """
            Enables the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["enabled"] = True
        
        def disable(self):
            """
            Disables the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["enabled"] = False
        
        def increment(self):
            """
            Increments the amount of times Monika has had the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["times_had"] += 1
        
        def shouldHave(self, _now=None):
            """
            Checks if we should have this consumable now

            CONDITIONS:
                1. We're within the consumable time range
                2. We pass the chance check to have this consumable
                3. We have not met/exceeded the maximum re-serve amount

            IN:
                _now - datetime.datetime to check if we're within the timerange for this consumable
                If None, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we should have this consumable (passes above conditions)
                    - False otherwise

            NOTE: This does NOT anticipate splits/preparation
            """
            
            if self.max_re_serve is not None and self.re_serves_had == self.max_re_serve:
                return False
            
            if _now is None:
                _now = datetime.datetime.now()
            
            _chance = random.randint(1, 100)
            
            for start_time, end_time in self.start_end_tuple_list:
                if start_time <= _now.hour < end_time and _chance <= self.cons_chance:
                    return True
            return False
        
        def hasServing(self):
            """
            Checks if we have a serving of this consumable in order to use it

            OUT:
                boolean:
                    - True if we have at least 1 serving left of the consumable
                    - False otherwise
            """
            return persistent._mas_consumable_map[self.consumable_id]["servings_left"] > 0
        
        def restock(self, servings=100, clear_flag=True):
            """
            Adds more servings of the consumable, protected by max_stock_amount

            IN:
                servings - amount of servings to add
                (Default: 100)
                clear_flag - whether or not we should clear the has_restock_warned flag
                (Default: True)
            """
            max_to_add = self.max_stock_amount - self.getStock()
            
            
            servings = max_to_add if servings > max_to_add else servings
            
            persistent._mas_consumable_map[self.consumable_id]["servings_left"] += servings
            
            if clear_flag:
                self.resetRestockWarnFlag()
        
        def getStock(self):
            """
            Gets the amount of servings left of a consumable

            OUT:
                integer:
                    - The amount of servings left for the consumable
            """
            return persistent._mas_consumable_map[self.consumable_id]["servings_left"]
        
        def isMaxedStock(self):
            """
            Checks if the current stock of the consumable is the max

            OUT:
                boolean:
                    - True if stock is maxed
                    - False otherwise
            """
            return self.getStock() == self.max_stock_amount
        
        def getAmountHad(self):
            """
            Gets the amount of servings Monika has had of the consumable

            OUT:
                integer:
                    - The amount of times Monika has had the consumable
            """
            return persistent._mas_consumable_map[self.consumable_id]["times_had"]
        
        def isLow(self):
            """
            Checks if we're running low on a consumable

            OUT:
                boolean:
                    - True if we're less than or equal to the LOW_STOCK_AMT value
                    - False otherwise
            """
            return self.getStock() <= MASConsumable.LOW_STOCK_AMT
        
        def isCriticalLow(self):
            """
            Checks if we're critically low on a consumable

            OUT:
                boolean:
                    - True if we're less than or equal to the LOW_CRITICAL_STOCK_AMT value
                    - False otherwise
            """
            return self.getStock() <= MASConsumable.LOW_CRITICAL_STOCK_AMT
        
        def flagRestockWarn(self):
            """
            Flags a consumable as having been restock warned
            """
            persistent._mas_consumable_map[self.consumable_id]["has_restock_warned"] = True
        
        def resetRestockWarnFlag(self):
            """
            Resets the restock warn flag
            """
            persistent._mas_consumable_map[self.consumable_id]["has_restock_warned"] = False
        
        def hasRestockWarned(self):
            """
            Return the has restock warned flag
            """
            return persistent._mas_consumable_map[self.consumable_id]["has_restock_warned"]
        
        def use(self, amount=1):
            """
            Uses a serving of this consumable

            IN:
                amount - amount of servings to use up
                (Default: 1)
            """
            servings_left = persistent._mas_consumable_map[self.consumable_id]["servings_left"]
            
            if servings_left - amount < 0:
                persistent._mas_consumable_map[self.consumable_id]["servings_left"] = 0
            else:
                persistent._mas_consumable_map[self.consumable_id]["servings_left"] -= amount
        
        def re_serve(self):
            """
            Increments the re-serve count
            """
            self.re_serves_had += 1
        
        def isLateEntry(self, _now=None):
            """
            Checks if we should load with a consumable already out or not

            IN:
                _now - datetime.datetime to check if we're within the time for the consumable
                If None, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we should load in with consumable already out
                    - False otherwise
            """
            if _now is None:
                _now = datetime.datetime.now()
            
            for index in range(len(self.start_end_tuple_list)):
                
                _start, _end = self.start_end_tuple_list[index]
                late_hour = self.late_entry_list[index]
                
                if (
                    _start <= _now.hour < _end
                    and _now.hour >= late_hour
                ):
                    return True
            return False
        
        def prepare(self, _start_time=None):
            """
            Starts preparing the consumable
            (Sets up the finished preparing event)

            IN:
                _start_time - time to start prepping. If none, now is assumed
            """
            if _start_time is None:
                _start_time = datetime.datetime.now()
            
            
            persistent._mas_current_consumable[self.consumable_type]["prep_time"] = _start_time
            
            
            end_prep = random.randint(self.prep_low, self.prep_high)
            
            
            mas_setEVLPropValues(
                self.finish_prep_evl,
                conditional=(
                    "persistent._mas_current_consumable[{0}]['prep_time'] is not None "
                    "and (datetime.datetime.now() - "
                    "persistent._mas_current_consumable[{0}]['prep_time']) "
                    "> datetime.timedelta(0, {1})"
                ).format(self.consumable_type, end_prep),
                action=EV_ACT_QUEUE
            )
            
            
            persistent._mas_current_consumable[self.consumable_type]["id"] = self.consumable_id
        
        def have(self, _start_time=None, skip_leadin=False):
            """
            Allows Monika to have this consumable
            (Sets up the finished consumable event)

            IN:
                _start_time - time to start prepping. If none, now is assumed
                skip_leadin - whether or not we should push the event where Monika gets something to have
            """
            if _start_time is None:
                _start_time = datetime.datetime.now()
            
            
            consumable_time = datetime.timedelta(0, random.randint(self.cons_low, self.cons_high))
            
            
            persistent._mas_current_consumable[self.consumable_type]["consume_time"] = _start_time + consumable_time
            
            
            mas_setEVLPropValues(
                self.finish_cons_evl,
                conditional=(
                    "persistent._mas_current_consumable[{0}]['consume_time'] is not None "
                    "and datetime.datetime.now() > persistent._mas_current_consumable[{0}]['consume_time']"
                ).format(self.consumable_type),
                action=EV_ACT_QUEUE
            )
            
            
            if skip_leadin:
                persistent._mas_current_consumable[self.consumable_type]["id"] = self.consumable_id
                monika_chr.wear_acs(self.acs)
            
            
            elif not self.prepable() and not MASConsumable._m1_zz_consumables__getCurrentConsumable(self.consumable_type):
                persistent._mas_current_consumable[self.consumable_type]["id"] = self.consumable_id
                queueEvent(self.get_cons_evl)
            
            
            self.increment()
        
        def isConsTime(self, _now=None):
            """
            Checks if we're in the time range for this consumable

            IN:
                _now - datetime.datetime to check if we're within the time for
                    If None, now is assumed
                    (Default: None)

            OUT:
                boolean:
                    - True if we're within the consumable time(s) of this consumable
                    - False otherwise
            """
            if _now is None:
                _now = datetime.datetime.now()
            
            for start_time, end_time in self.start_end_tuple_list:
                if start_time <= _now.hour < end_time:
                    return True
            return False
        
        def shouldPrep(self, _now=None):
            """
            Checks if we're in the time range for this consumable and we should prepare it

            IN:
                _time - datetime.datetime to check if we're within the time for
                    If none, now is assumed
                    (Default: None)

            OUT:
                boolean:
                    - True if we're within the preparation time(s) of this consumable (and consumable is preparable)
                    - False otherwise
            """
            if not self.prepable():
                return False
            
            if _now is None:
                _now = datetime.datetime.now()
            
            _chance = random.randint(1, 100)
            
            for split in self.split_list:
                if _now.hour < split and _chance <= self.cons_chance:
                    return True
            return False
        
        def prepable(self):
            """
            Checks if this consumable is preparable

            OUT:
                boolean:
                    - True if this consumable has:
                        1. prep_high
                        2. prep_low

                    - False otherwise
            """
            return self.prep_low is not None and self.prep_high is not None
        
        def checkCanHave(self, _now=None):
            """
            Checks if we can have this consumable again

            IN:
                _now - datetime.datetime to check against
                    If None, now is assumed
                    (Default: None)

            OUT:
                boolean:
                    - True if we can have this consumable
                    - False otherwise
            """
            
            if self.done_cons_until is None:
                return True
            
            
            elif _now is None:
                _now = datetime.datetime.now()
            
            if _now >= self.done_cons_until:
                self.done_cons_until = None
                return True
            return False
        
        @staticmethod
        def _isStillCons(_type, _now=None):
            """
            Checks if we're still having something

            IN:
                _type - Type of consumable to check for
                    0 - Drink
                    1 - Food

                _now - datetime.datetime object representing current time
                    If none, now is assumed
                    (Default: None)

            OUT:
                boolean:
                    - True if we're still having something
                    - False otdherwise
            """
            if _now is None:
                _now = datetime.datetime.now()
            
            _time = persistent._mas_current_consumable[_type]["consume_time"]
            return _time is not None and _now < _time
        
        @staticmethod
        def _getLowCons(critical=False):
            """
            Gets a list of all consumables which Monika is low on, regardless of type (and should warn about)

            IN:
                - critical - Whether this list should only be populated by items Monika is critically low on or not
                    (Default: False)

            OUT:
                list of all consumables Monika is low on (or critical on)
            """
            low_cons = []
            for _type in store.mas_consumables.consumable_map.iterkeys():
                low_cons += MASConsumable._getLowConsType(_type, critical)
            
            return low_cons
        
        @staticmethod
        def _getLowConsNotWarned(critical=False):
            """
            Gets a list of all consumables which Monika is low on that she's not restock warned

            IN:
                - critical - Whether this list should only be populated by items Monika is critically low on or not
                    (Default: False)

            OUT:
                list of all consumables Monika
            """
            low_cons = []
            for _type in store.mas_consumables.consumable_map.iterkeys():
                low_cons += MASConsumable._getLowConsType(_type, critical, exclude_restock_warned=True)
            
            return low_cons
        
        @staticmethod
        def _getLowConsType(_type, critical=False, exclude_restock_warned=False):
            """
            Gets a list of all consumables (of the provided type) which Monika is low on (and should warn about)

            IN:
                _type - Type of consumables to get a low list for
                critical - Whether the list should be only those Monika is critically low on
                    (Default: False)
                exclude_restock_warned - Whether or not we want to exclude consumables we've restock warned already
                    (Default: False)

            OUT:
                list of all consumables of the provided type Monika is low on (or critical on), matching the entered criteria
            """
            if _type not in store.mas_consumables.consumable_map:
                return []
            
            if critical:
                if exclude_restock_warned:
                    return [
                        cons
                        for cons in store.mas_consumables.consumable_map[_type].itervalues()
                        if cons.enabled() and cons.should_restock_warn and cons.isCriticalLow() and not cons.hasRestockWarned()
                    ]
                
                else:
                    return [
                        cons
                        for cons in store.mas_consumables.consumable_map[_type].itervalues()
                        if cons.enabled() and cons.should_restock_warn and cons.isCriticalLow()
                    ]
            
            else:
                if exclude_restock_warned:
                    return [
                        cons
                        for cons in store.mas_consumables.consumable_map[_type].itervalues()
                        if cons.enabled() and cons.should_restock_warn and cons.isLow() and not cons.hasRestockWarned()
                    ]
                
                else:
                    return [
                        cons
                        for cons in store.mas_consumables.consumable_map[_type].itervalues()
                        if cons.enabled() and cons.should_restock_warn and cons.isLow()
                    ]
        
        @staticmethod
        def _reset(_type=None):
            """
            Resets the events for the consumable and resets the current consumable(s)

            IN:
                _type - Type of consumable to reset events for
                    (If None, all types are reset. Default: None)
            """
            def cons_reset(consumable):
                """
                Resets the labels for the current consumables

                IN:
                    consumable - consumable object to reset
                """
                if consumable is None:
                    return
                
                monika_chr.remove_acs(consumable.acs)
                consumable.re_serves_had = 0
                
                
                mas_stripEVL(consumable.get_cons_evl, list_pop=True)
                mas_stripEVL(consumable.finish_prep_evl, list_pop=True)
                mas_stripEVL(consumable.finish_cons_evl, list_pop=True)
                
                
                persistent._mas_current_consumable[consumable.consumable_type] = {
                    "prep_time": None,
                    "consume_time": None,
                    "id": None
                }
            
            
            if _type == 0 or _type is None:
                cons_reset(MASConsumable._getCurrentDrink())
            
            if _type ==1 or _type is None:
                cons_reset(MASConsumable._getCurrentFood())
        
        @staticmethod
        def _m1_zz_consumables__shouldReset(_type, curr_cons, available_cons):
            """
            Checks if we should reset the current consumable type

            CONDITIONS:
                1. We're having a consumable we shouldn't be having now and we opened the game after its consume time or
                2. We're still prepping something but
                    - The consumable's finish prepping event doesn't have conditionals or
                    - It's no longer time for this consumable

            IN:
                _type - type of consumable to reset
                curr_cons - current_consumable (of _type)
                available_cons - available consumables for the current time

            OUT:
                boolean:
                    - True if we should reset the current consumable type
                    - False otherwise
            """
            
            if not curr_cons:
                return False
                        
            return (
                (
                    MASConsumable._isHaving(_type)
                    and (
                        not MASConsumable._isStillCons(_type)
                        and mas_getCurrSeshStart() > persistent._mas_current_consumable[_type]["consume_time"]
                    )
                )
                or (
                    persistent._mas_current_consumable[_type]["prep_time"] is not None
                    and (
                        mas_checkEVL(curr_cons.finish_prep_evl, lambda x: x.conditional is None)
                        or curr_cons not in available_cons
                    )
                )
            )
        
        @staticmethod
        def _getCurrentDrink():
            """
            Gets the MASConsumable object for the current drink or None if we're not drinking

            OUT:
                - Current MASConsumable if drinking
                - None if not drinking
            """
            return MASConsumable._m1_zz_consumables__getCurrentConsumable(store.mas_consumables.TYPE_DRINK)
        
        @staticmethod
        def _getCurrentFood():
            """
            Gets the MASConsumable object for the current food or None if we're not eating

            OUT:
                - Current MASConsumable if eating
                - None if not eating
            """
            return MASConsumable._m1_zz_consumables__getCurrentConsumable(store.mas_consumables.TYPE_FOOD)
        
        @staticmethod
        def _isHaving(_type):
            """
            Checks if we're currently drinking something right now

            IN:
                _type - integer representing the consumable type

            OUT:
                boolean:
                    - True if we have a current consumable of _type and consume time
                    - False otherwise
            """
            return (
                bool(
                    persistent._mas_current_consumable[_type]["id"]
                    and persistent._mas_current_consumable[_type]["consume_time"]
                )
            )
        
        @staticmethod
        def _getConsumablesForTime(_type):
            """
            Gets a list of all consumable drinks active at this time

            IN:
                _type - type of consumables to get

            OUT:
                list of consumable objects of _type enabled and within time range
            """
            if _type not in store.mas_consumables.consumable_map:
                return []
            
            return [
                cons
                for cons in mas_consumables.consumable_map[_type].itervalues()
                if cons.enabled() and cons.hasServing() and cons.checkCanHave() and cons.isConsTime()
            ]
        
        @staticmethod
        def _validatePersistentData(_type):
            """
            Verifies that the data stored in persistent._mas_current_consumable is valid to the consumables currently set up

            IN:
                _type - type of consumable to validate persistent data for

            NOTE: If the persistent data stored isn't valid, it is reset.
            """
            if MASConsumable._isHaving(_type) and not MASConsumable._m1_zz_consumables__getCurrentConsumable(_type):
                persistent._mas_current_consumable[_type] = {
                    "prep_time": None,
                    "consume_time": None,
                    "id": None
                }
        
        @staticmethod
        def _checkConsumables(startup=False):
            """
            Logic to handle Monika having a consumable both on startup and during runtime

            IN:
                startup - Whether or not we should check for a late entry
                (Default: False)
            """
            MASConsumable._m1_zz_consumables__checkingLogic(
                _type=store.mas_consumables.TYPE_DRINK,
                curr_cons=MASConsumable._getCurrentDrink(),
                startup=startup
            )
            
            MASConsumable._m1_zz_consumables__checkingLogic(
                _type=store.mas_consumables.TYPE_FOOD,
                curr_cons=MASConsumable._getCurrentFood(),
                startup=startup
            )
            
            if startup and not store.mas_globals.returned_home_this_sesh:
                MASConsumable._absentUse()
                
                
                drink_acs = store.monika_chr.get_acs_of_exprop(store.mas_sprites.EXP_A_DRINK)
                food_acs = store.monika_chr.get_acs_of_exprop(store.mas_sprites.EXP_A_FOOD)
                
                
                if not MASConsumable._isHaving(store.mas_consumables.TYPE_DRINK) and drink_acs:
                    store.monika_chr.remove_acs(drink_acs)
                
                if not MASConsumable._isHaving(store.mas_consumables.TYPE_FOOD) and food_acs:
                    store.monika_chr.remove_acs(food_acs)
                
                
                if MASConsumable._getLowConsNotWarned():
                    store.queueEvent("mas_consumables_generic_running_out_absentuse")
        
        @staticmethod
        def _absentUse():
            """
            Runs a check on all consumables and subtracts the amount used in the player's absence
            """
            def calculate_and_use(consumable, servings, days_absent):
                """
                Checks how many servings of the consumable Monika will have used in the player's absence

                IN:
                    consumable - consumable to use
                    servings - amount of servings per having of the consumable
                    days_absent - amount of days the player was absent
                """
                chance = random.randint(1, 100)
                for day in range(days_absent):
                    if chance <= consumable.cons_chance:
                        consumable.use(servings)
            
            
            consumables = MASConsumable._getEnabledConsumables()
            _days = mas_getAbsenceLength().days
            
            for cons in consumables:
                if cons.prepable():
                    calculate_and_use(consumable=cons, servings=random.randint(3,5), days_absent=_days)
                else:
                    calculate_and_use(consumable=cons, servings=4, days_absent=_days)
        
        @staticmethod
        def _getEnabledConsumables():
            """
            Gets all enabled consumables

            OUT:
                List of MASConsumable objects which are enabled

            NOTE: enabled is regardless of stock amount
            """
            consumables = []
            
            if store.mas_consumables.TYPE_DRINK in store.mas_consumables.consumable_map:
                consumables.extend([
                    drink
                    for drink in store.mas_consumables.consumable_map[mas_consumables.TYPE_DRINK].values()
                    if drink.enabled()
                ])
            
            if store.mas_consumables.TYPE_FOOD in store.mas_consumables.consumable_map:
                consumables.extend([
                    food
                    for food in store.mas_consumables.consumable_map[mas_consumables.TYPE_FOOD].values()
                    if food.enabled()
                ])
            
            return consumables
        
        @staticmethod
        def _m1_zz_consumables__getCurrentConsumable(_type):
            """
            Gets the current consumable, provided by type

            IN:
                _type - consumable type to get the current consumable for

            OUT:
                MASConsumable object representing the current consumable object for the type
                If there's no consumable out by _type, None is returned
            """
            return mas_getConsumable(
                persistent._mas_current_consumable[_type]["id"]
            )
        
        @staticmethod
        def _m1_zz_consumables__checkingLogic(_type, curr_cons, startup):
            """
            Generalized logic to check if we should have a consumable

            IN:
                _type - consumable type
                curr_cons - current_consumable (of _type)
                startup - whether or not to perform a startup check
            """
            available_cons = MASConsumable._getConsumablesForTime(_type)
            
            
            MASConsumable._validatePersistentData(_type)
            
            
            if MASConsumable._m1_zz_consumables__shouldReset(_type, curr_cons, available_cons):
                MASConsumable._reset(_type)
            
            
            if persistent._mas_current_consumable[_type]["id"] is not None:
                
                if MASConsumable._isHaving(_type) and not monika_chr.is_wearing_acs(curr_cons.acs):
                    monika_chr.wear_acs(curr_cons.acs)
                return
            
            
            if not available_cons:
                return
            
            
            cons = random.choice(available_cons)
            
            
            _now = datetime.datetime.now()
            
            
            
            MASConsumable._reset(_type)
            
            
            if cons.shouldHave():
                
                if cons.prepable():
                    cons.use(amount=random.randint(3,5))
                
                
                else:
                    cons.use()
                
                
                
                if startup and cons.isLateEntry() and random.randint(1, 100) <= 80:
                    cons.have(skip_leadin=True)
                
                else:
                    
                    if cons.prepable() and cons.shouldPrep(_now):
                        cons.prepare()
                    
                    
                    elif not cons.prepable():
                        cons.have()




    def mas_generateShoppingList(low_cons_list=None):
        """
        Generates a list of consumables we're low on in the form of a 'shopping list'
        and exports it to the characters folder

        IN:
            low_cons_list - List of MASConsumable objects that we're low on
            If None, we get it here
            (Default: None)
        """
        
        if low_cons_list is None:
            low_cons_list = MASConsumable._getLowCons()
        
        START_TEXT = (
            "Привет, [player],\n"
            "Просто сообщаю, что мне не хватает нескольких вещей.\n"
            "Ты не против получить ещё немного вещей для меня, не так ли?\n\n"
            "Вот список того, что у меня закончилось:\n"
        )
        
        MID_TEXT = ""
        
        END_TEXT = (
            "Спасибо, [player]~"
        )
        
        for cons in low_cons_list:
            MID_TEXT += "- {0}\n".format(cons.disp_name.capitalize())
        
        MID_TEXT += "\n"
        
        with open(user_dir + "/characters/shopping_list.txt", "w") as shopping_list:
            shopping_list.write(
                renpy.substitute(START_TEXT + MID_TEXT + END_TEXT)
            )

    def mas_getConsumable(consumable_id):
        """
        Gets a consumable object by type and id

        IN:
            consumable_id - id of the consumable

        OUT:
            Consumable object:
                If found, MASConsumable
                If not found, None
        """
        for consumable_type in store.mas_consumables.consumable_map.keys():
            if consumable_id in store.mas_consumables.consumable_map[consumable_type]:
                return store.mas_consumables.consumable_map[consumable_type][consumable_id]
        return None

    def mas_useThermos():
        """
        Gets Monika to put her drink into a thermos when taking her somewhere if it is eligible
        """
        
        if monika_chr.is_wearing_acs_type("thermos-mug"):
            return
        
        
        current_drink = MASConsumable._getCurrentDrink()
        if current_drink and current_drink.portable:
            
            thermoses = [thermos.get_sprobj() for thermos in mas_selspr.filter_acs(True, "thermos-mug")]
            
            
            if thermoses:
                thermos = renpy.random.choice(thermoses)
                monika_chr.wear_acs(thermos)


init 6 python:
    MASConsumable(
        consumable_id="coffee",
        consumable_type=store.mas_consumables.TYPE_DRINK,
        disp_name="coffee",
        dlg_props=mas_consumables.DLG_PREP_HOT_DRINK,
        start_end_tuple_list=[(5, 12)],
        acs=mas_acs_mug,
        portable=True,
        split_list=[11],
        late_entry_list=[10],
        max_re_serve=3
    )

    MASConsumable(
        consumable_id="hotchoc",
        consumable_type=store.mas_consumables.TYPE_DRINK,
        disp_name="hot chocolate",
        dlg_props=mas_consumables.DLG_PREP_HOT_DRINK,
        start_end_tuple_list=[(16,23)],
        acs=mas_acs_hotchoc_mug,
        portable=True,
        split_list=[22],
        late_entry_list=[19],
        max_re_serve=3
    )

    MASConsumable(
        consumable_id="candycane",
        consumable_type=store.mas_consumables.TYPE_FOOD,
        disp_name="candycane",
        dlg_props={
            mas_consumables.PROP_PLUR: True
        },
        start_end_tuple_list=[(11,14), (16, 20)],
        acs=mas_acs_candycane,
        split_list=[12, 18],
        late_entry_list=[13, 19],
        max_re_serve=2,
        should_restock_warn=False,
        max_stock_amount=18,
        prep_low=None,
        cons_high=15*60, 
        
        finish_cons_evl="mas_consumables_candycane_finish_having"
    )

    MASConsumable(
        consumable_id="christmascookies",
        consumable_type=store.mas_consumables.TYPE_FOOD,
        disp_name="Christmas cookie",
        dlg_props={
            mas_consumables.PROP_OBJ_REF: "plate",
            mas_consumables.PROP_PLUR: True
        },
        start_end_tuple_list=[(11,14), (16, 22)],
        acs=mas_acs_christmascookies,
        split_list=[12, 18],
        late_entry_list=[13, 19],
        max_re_serve=2,
        should_restock_warn=False,
        max_stock_amount=20,
        prep_low=None,
        cons_high=30*60
    )



init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_brewing",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_finished_brewing:
    $ current_drink = MASConsumable._getCurrentDrink()
    call mas_consumables_generic_finished_prepping (consumable=current_drink) from _call_mas_consumables_generic_finished_prepping
    return


init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_drinking",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_finished_drinking:

    $ current_drink = MASConsumable._getCurrentDrink()
    call mas_consumables_generic_finish_having (consumable=current_drink) from _call_mas_consumables_generic_finish_having
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_get_drink",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_get_drink:
    $ current_drink = MASConsumable._getCurrentDrink()
    call mas_consumables_generic_get (consumable=current_drink) from _call_mas_consumables_generic_get
    return



init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_prepping",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_finished_prepping:
    $ current_food = MASConsumable._getCurrentFood()
    call mas_consumables_generic_finished_prepping (consumable=current_food) from _call_mas_consumables_generic_finished_prepping_1
    return



init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_eating",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_finished_eating:

    $ current_food = MASConsumable._getCurrentFood()
    call mas_consumables_generic_finish_having (consumable=current_food) from _call_mas_consumables_generic_finish_having_1
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_get_food",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_get_food:
    $ current_food = MASConsumable._getCurrentFood()
    call mas_consumables_generic_get (consumable=current_food) from _call_mas_consumables_generic_get_1
    return


default persistent.msr_disp_name = "кофе"

label mas_consumables_generic_get(consumable):
    if consumable.disp_name == 'coffee':
        $ persistent.msr_disp_name = 'кофе'
    elif consumable.disp_name == 'Christmas cookie':
        $ persistent.msr_disp_name = 'рождественского печенья'
    elif consumable.disp_name == 'candycane':
        $ persistent.msr_disp_name = 'сахарную тросточку'
    else:
        $ persistent.msr_disp_name = 'горячего шоколада'
    
    
    python:
        dlg_props = consumable.dlg_props

        container = dlg_props.get(mas_consumables.PROP_CONTAINER)
        obj_ref = dlg_props.get(mas_consumables.PROP_OBJ_REF)
        plur = "s" if dlg_props.get(mas_consumables.PROP_PLUR, False) else ""

        if not consumable.disp_name == 'Christmas cookie' and not consumable.disp_name == 'candycane':
            if container:
                line_starter = renpy.substitute("Пойду, возьму себе чашку [persistent.msr_disp_name].")


            elif obj_ref:
                line_starter = renpy.substitute("Пойду, возьму себе чашку [persistent.msr_disp_name].")
            

            else:
                
                a_an = "немного" if plur else mas_a_an(consumable.disp_name, ignore_case=True)
                line_starter = renpy.substitute("Пойду, возьму себе [a_an] [persistent.msr_disp_name].")
        
        else:

            if consumable.disp_name == 'Christmas cookie':
                line_starter = renpy.substitute("Пойду, возьму себе тарелку [persistent.msr_disp_name].")

            else:
                line_starter = renpy.substitute("Пойду, возьму себе [persistent.msr_disp_name].")

    
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "[line_starter] Скоро вернусь.{w=1}{nw}"
    else:

        m 1eua "[line_starter]"
        $ MAS.MonikaElastic()
        m 1eua "Секундочку."


    if (
        consumable.consumable_type == store.mas_consumables.TYPE_FOOD
        and monika_chr.is_wearing_acs(mas_acs_quetzalplushie)
    ):
        $ mas_acs_quetzalplushie.keep_on_desk = False


    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_1


    python:
        renpy.pause(1.0, hard=True)
        consumable.acs.keep_on_desk = False
        monika_chr.remove_acs(mas_acs_quetzalplushie)
        monika_chr.wear_acs(consumable.acs)
        renpy.pause(4.0, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_5
    $ consumable.acs.keep_on_desk = True

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        $ MAS.MonikaElastic()
        m 1hua "Я тут!{w=1.5}{nw}"
    else:

        $ MAS.MonikaElastic()
        m 1eua "Ладно, какие у нас ещё планы на сегодня?"
    return

label mas_consumables_generic_finish_having(consumable):
    python:
        get_more = (
            consumable.shouldHave()
            and (consumable.prepable() or (not consumable.prepable() and consumable.hasServing()))
        )

        dlg_props = consumable.dlg_props

        container = dlg_props.get(mas_consumables.PROP_CONTAINER)
        obj_ref = dlg_props.get(mas_consumables.PROP_OBJ_REF)
        plur = "s" if dlg_props.get(mas_consumables.PROP_PLUR, False) else ""

        dlg_map = {
            mas_consumables.PROP_CONTAINER: {
                0: "Я собираюсь убрать эту чашку.",
                1: "Я собираюсь взять ещё одну чашку."
            },
            mas_consumables.PROP_OBJ_REF: {
                0: "Я собираюсь убрать это подальше.",
                1: "Я собираюсь взять ещё один кусочек."
            },
            "else": {
                0: "Я собираюсь это убрать.",
                1: "Я собираюсь взять ещё один."
            }
        }


        if container:
            line_starter = renpy.substitute(dlg_map[mas_consumables.PROP_CONTAINER][get_more])


        elif obj_ref:
            line_starter = renpy.substitute(dlg_map[mas_consumables.PROP_OBJ_REF][get_more])


        else:
            line_starter = renpy.substitute(dlg_map["else"][get_more])

    if consumable.disp_name == 'coffee':
        $ persistent.msr_disp_name = 'кофе'
    elif consumable.disp_name == 'hot chocolate':
        $ persistent.msr_disp_name = 'горячий шоколад'
    elif consumable.disp_name == 'Christmas cookie':
        $ persistent.msr_disp_name = 'рождественское печенье'
    else:
        $ persistent.msr_disp_name = 'сахарную тросточку'
    
    if consumable.disp_name == 'coffee' or consumable.disp_name == 'hot chocolate':
        $ finished = "допила"
        $ svoi = "свой"
    elif consumable.disp_name == 'Christmas cookie' or consumable.disp_name == 'candycane':
        $ finished = "доела"
        if consumable.disp_name == 'Christmas cookie':
            $ svoi = "своё"
        else:
            $ svoi = "свою"

    if (not mas_canCheckActiveWindow() or mas_isFocused()) and not store.mas_globals.in_idle_mode:
        $ MAS.MonikaElastic()
        m 1eud "Всё, я [finished] [svoi] [persistent.msr_disp_name].{w=0.2} {nw}"
        extend 1eua "[line_starter]"
        $ MAS.MonikaElastic()
        m 3eua "Секундочка."

    elif store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        $ MAS.MonikaElastic()
        m 1esd "О, я уже [finished] [svoi] [persistent.msr_disp_name].{w=1} {nw}"
        $ MAS.MonikaElastic()
        m 1eua "[line_starter] Скоро вернусь.{w=1}{nw}"


    $ consumable.acs.keep_on_desk = False
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_2


    python:
        renpy.pause(1.0, hard=True)


        if not get_more:
            
            MASConsumable._reset(consumable.consumable_type)
            
            consumable.done_cons_until = datetime.datetime.now() + MASConsumable.DEF_DONE_CONS_TD

        else:
            consumable.have()
            consumable.re_serve()
            
            
            if not consumable.prepable():
                consumable.use()

        renpy.pause(4.0, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_6
    $ consumable.acs.keep_on_desk = True

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        $ MAS.MonikaElastic()
        m 1hua "Я тут!{w=1.5}{nw}"

        if (
            not mas_inEVL("mas_consumables_generic_queued_running_out")
            and mas_getEV("mas_consumables_generic_queued_running_out").timePassedSinceLastSeen_d(datetime.timedelta(days=7))
            and len(MASConsumable._getLowCons()) > 0
        ):
            $ queueEvent("mas_consumables_generic_queued_running_out")


    elif not get_more and consumable.isCriticalLow() and consumable.should_restock_warn:
        call mas_consumables_generic_critical_low (consumable=consumable) from _call_mas_consumables_generic_critical_low


    elif not get_more and consumable.isLow() and consumable.should_restock_warn:
        call mas_consumables_generic_running_out (consumable=consumable) from _call_mas_consumables_generic_running_out
    else:

        $ MAS.MonikaElastic()
        m 1eua "Ладно, какие у нас ещё планы на сегодня?"
    return
    return

label mas_consumables_generic_finished_prepping(consumable):

    if (not mas_canCheckActiveWindow() or mas_isFocused()) and not store.mas_globals.in_idle_mode:
        if consumable.disp_name == 'coffee':
            $ persistent.msr_disp_name = 'кофе'
        elif consumable.disp_name == 'hot chocolate':
            $ persistent.msr_disp_name = 'горячий шоколад'
        elif consumable.disp_name == 'Christmas cookie':
            $ persistent.msr_disp_name = 'рождественское печенье'
        else:
            $ persistent.msr_disp_name = 'сахарную тросточку'
        
        if consumable.disp_name == 'coffee' or consumable.disp_name == 'hot chocolate':
            $ moi = "мой"
            $ gotov = "готов"
        elif consumable.disp_name == 'Christmas cookie' or consumable.disp_name == 'candycane':
            $ gotov = "теперь тут"
            if consumable.disp_name == 'Christmas cookie':
                $ moi = "моё"
            else:
                $ moi = "моя"
            
        if consumable.disp_name == 'coffee':
            $ persistent.msr_disp_name = 'кофе'
        else:
            $ persistent.msr_disp_name = 'горячий шоколад'
        m 1esd "О, [moi] [persistent.msr_disp_name] [gotov]."
        $ MAS.MonikaElastic()
        m 1eua "Секунду."
    else:


        if consumable.disp_name == 'coffee':
            $ persistent.msr_disp_name = 'кофе'
        elif consumable.disp_name == 'hot chocolate':
            $ persistent.msr_disp_name = 'горячего шоколада'
        elif consumable.disp_name == 'Christmas cookie':
            $ persistent.msr_disp_name = 'рождественского печенья'
        else:
            $ persistent.msr_disp_name = 'сахарную тросточку'
        
        if consumable.disp_name == 'coffee' or consumable.disp_name == 'hot chocolate':
            $ container = "чашку "
        elif consumable.disp_name == 'Christmas cookie' or consumable.disp_name == 'candycane':
            if consumable.disp_name == 'Christmas cookie':
                $ container = "тарелку "
            else:
                $ container = ""

        m 1eua "Пойду, возьму себе [container][persistent.msr_disp_name]. Скоро вернусь.{w=1}{nw}"



    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_3


    python:
        renpy.pause(1.0, hard=True)


        consumable.acs.keep_on_desk = False

        monika_chr.wear_acs(consumable.acs)


        persistent._mas_current_consumable[consumable.consumable_type]["prep_time"] = None

        consumable.have()

        renpy.pause(4.0, hard=True)


    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_7
    $ consumable.acs.keep_on_desk = True

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        $ MAS.MonikaElastic()
        m 1hua "Я тут!{w=1.5}{nw}"
    else:

        $ MAS.MonikaElastic()
        m 1eua "Ладно, какие у нас ещё планы на сегодня?"

    return

label mas_consumables_refill_explain:

    $ MAS.MonikaElastic()
    m 3rksdla "Я бы продублировала то, что имею сейчас... но когда я пробовала раньше, это было совсем не то..."
    $ MAS.MonikaElastic()
    m 1eksdla "Наверное, мне чего-то не хватает, потому что я просто не могу воспроизвести этот вкус."
    if mas_isMoniHappy(higher=True):
        $ MAS.MonikaElastic()
        m 1ekbsu "...Или, может быть, это твоя вечная любовь делает его особенным~"
    return

label mas_consumables_generic_running_out(consumable):
    $ amt_left = consumable.getStock()
    m 1euc "Между прочим, [player]..."
    if consumable.disp_name == 'coffee':
        $ persistent.msr_disp_name = 'кофе'
    elif consumable.disp_name == 'hot chocolate':
        $ persistent.msr_disp_name = 'горячего шоколада'
    elif consumable.disp_name == 'Christmas cookie':
        $ persistent.msr_disp_name = 'рождественского печенья'
    else:
        $ persistent.msr_disp_name = 'сахарную тросточку'
        
    if consumable.disp_name == 'coffee' or consumable.disp_name == 'hot chocolate':
        if amt_left == 1:
            $ container = "чашка "
        elif amt_left == 2 or amt_left == 3 or amt_left == 4:
            $ container = "чашки "
        else:
            $ container = "чашек "
    elif consumable.disp_name == 'Christmas cookie' or consumable.disp_name == 'candycane':
        if consumable.disp_name == 'Christmas cookie':
            if amt_left == 1:
                $ container = "тарелка "
            elif amt_left == 2 or amt_left == 3 or amt_left == 4:
                $ container = "тарелки "
            else:
                $ container = "тарелок "
        else:
            $ container = ""
            if amt_left == 1:
                $ persistent.msr_disp_name = "сахарная тросточка"
            elif amt_left == 2 or amt_left == 3 or amt_left == 4:
                $ persistent.msr_disp_name = "сахарные тросточки"
            else:
                $ persistent.msr_disp_name = "сахарных тросточек"

    if amt_left > 0:

        $ MAS.MonikaElastic()
        m 3eud "Я просто хотела дать тебе знать, что у меня осталась только [amt_left] [container][persistent.msr_disp_name]."

        if not renpy.seen_label("mas_consumables_refill_explain"):
            call mas_consumables_refill_explain from _call_mas_consumables_refill_explain
    else:

        if consumable.disp_name == 'coffee':
            $ finished = "кончился"
            $ persistent.msr_disp_name = 'кофе'
        elif consumable.disp_name == 'Christmas cookie':
            $ finished = "кончилось"
            $ persistent.msr_disp_name = 'рождественское печенье'
        elif consumable.disp_name == 'candycane':
            $ finished = "кончились"
            $ persistent.msr_disp_name = 'сахарные тросточки'
        else:
            $ finished = "кончился"
            $ persistent.msr_disp_name = 'горячий шоколад'
        $ MAS.MonikaElastic()
        m 3eud "Я просто хотела сказать тебе, что у меня [finished] [persistent.msr_disp_name]."

    $ MAS.MonikaElastic()
    m 1eka "Ты ведь не откажешься принести мне ещё, правда?"
    return

label mas_consumables_generic_critical_low(consumable):
    if consumable.disp_name == 'coffee':
        $ persistent.msr_disp_name = 'кофе'
    elif consumable.disp_name == 'Christmas cookie':
        $ persistent.msr_disp_name = 'рождественского печенья'
    elif consumable.disp_name == 'candycane':
        $ persistent.msr_disp_name = 'сахарная тросточка'
    else:
        $ persistent.msr_disp_name = 'горячего шоколада'
    
    if consumable.disp_name == 'coffee' or consumable.disp_name == 'hot chocolate':
        $ container = "чашка"
    elif consumable.disp_name == 'Christmas cookie':
        $ container = "тарелка "
    else:
        $ container = ""
    m 1euc "Эй, [player]..."
    $ MAS.MonikaElastic()
    m 3eua "У меня осталась только одна [container][persistent.msr_disp_name]."
    if not renpy.seen_label("mas_consumables_refill_explain"):
        call mas_consumables_refill_explain from _call_mas_consumables_refill_explain_1

    $ MAS.MonikaElastic()
    m 3eka "Не мог[mas_gender_g] бы ты как-нибудь принести мне ещё?"
    $ MAS.MonikaElastic()
    m 1hua "Спасибо~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_consumables_generic_queued_running_out"
        )
    )

label mas_consumables_generic_queued_running_out:
    $ low_cons = MASConsumable._getLowCons()
    call mas_consumables_generic_queued_running_out_dlg (low_cons) from _call_mas_consumables_generic_queued_running_out_dlg
    return "no_unlock"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_consumables_generic_running_out_absentuse"
        )
    )

label mas_consumables_generic_running_out_absentuse:
    $ low_cons = MASConsumable._getLowConsNotWarned()
    call mas_consumables_generic_queued_running_out_dlg (low_cons) from _call_mas_consumables_generic_queued_running_out_dlg_1
    return "no_unlock"


label mas_consumables_generic_queued_running_out_dlg(low_cons):

    if not low_cons:
        return

    m 1esc "Между прочим, [player]..."
    $ MAS.MonikaElastic()
    if len(low_cons) > 2:
        $ mas_generateShoppingList(low_cons)
        m 3rksdla "У меня тут кое-что кончилось..."
        $ MAS.MonikaElastic()
        m 3eua "Так что, надеюсь, ты не возражаешь, но я оставила тебе список вещей в папке characters."
        $ them = "их"
    else:
        python:
            # items_running_out_of = ""
            # if len(low_cons) == 2:
            #     items_running_out_of = "{0} и {1}".format(low_cons[0].disp_name, low_cons[1].disp_name)
            # else:
            #     items_running_out_of = low_cons[0].disp_name

            if len(low_cons) == 2:
                first_low_cons = low_cons[0].disp_name
                first_low_cons = (first_low_cons.replace("coffee", "кофе")
                .replace("hot chocolate", "горячий шоколад")
                .replace("Christmas cookie", "рождественское печенье")
                .replace("candycane", "сахарная тросточка")
                )

                second_low_cons = low_cons[1].disp_name
                second_low_cons = (second_low_cons.replace("coffee", "кофе")
                .replace("hot chocolate", "горячий шоколад")
                .replace("Christmas cookie", "рождественское печенье")
                .replace("candycane", "сахарная тросточка")
                )

            else:
                first_low_cons = low_cons[0].disp_name
                first_low_cons = (first_low_cons.replace("coffee", "кофе")
                .replace("hot chocolate", "горячий шоколад")
                .replace("Christmas cookie", "рождественское печенье")
                .replace("candycane", "сахарная тросточка")
                )

        if len(low_cons) == 2:
            m 3rksdla "У меня кончились [first_low_cons] и [second_low_cons]."
        else:
            if first_low_cons == 'кофе' or first_low_cons == 'горячий шоколад':
                m 3rksdla "У меня кончился [first_low_cons]."
            elif first_low_cons == 'рождественское печенье':
                m 3rksdla "У меня кончилось [first_low_cons]."
            else:
                m 3rksdla "У меня кончилась [first_low_cons]."

        # # комбинация с кофе
        # if items_running_out_of == 'coffee and hot chocolate':

        #     m 3rksdla "У меня кончились кофе и горячий шоколад."

        # elif items_running_out_of == 'coffee and Christmas cookie':

        #     m 3rksdla "У меня кончились кофе и рождественское печенье."

        # elif items_running_out_of == 'coffee and candycane':

        #     m 3rksdla "У меня кончились кофе и сахарная тросточка."
        # ##################
        # #комбинация с горячим шоколадом
        # elif items_running_out_of == 'hot chocolate and coffee':
            
        #     m 3rksdla "У меня кончились горячий шоколад и кофе."

        # elif items_running_out_of == 'hot chocolate and Christmas cookie':

        #     m 3rksdla "У меня кончились горячий шоколад и рождественское печенье."
        
        # elif items_running_out_of == 'hot chocolate and candycane':

        #     m 3rksdla "У меня кончились горячий шоколад и сахарная тросточка."
        # ##################
        # #комбинация с рождественским печеньем
        # elif items_running_out_of == 'Christmas cookie and coffee':

        #     m 3rksdla "У меня кончились рождественское печенье и кофе."
        
        # elif items_running_out_of == 'Christmas cookie and hot chocolate':

        #     m 3rksdla "У меня кончились рождественское печенье и горячий шоколад."

        # elif items_running_out_of == 'Christmas cookie and candycane':

        #     m 3rksdla "У меня кончились рождественское печенье и сахарная тросточка."
        # ##################
        # #комбинация с сахарной тросточкой
        # elif items_running_out_of == 'candycane and coffee':

        #     m 3rksdla "У меня кончились сахарная тросточка и кофе."
        
        # elif items_running_out_of == 'candycane and Christmas cookie':

        #     m 3rksdla "У меня кончились сахарная тросточка и рождественское печенье."

        # elif items_running_out_of == 'candycane and hot chocolate':

        #     m 3rksdla "У меня кончились сахарная тросточка и горячий шоколад."
        # ##################
        # #без комбинаций
        # elif items_running_out_of == 'candycane':

        #     m 3rksdla "У меня кончилась сахарная тросточка."

        # elif items_running_out_of == 'Christmas cookie':

        #     m 3rksdla "У меня кончилось рождественское печенье."

        # elif items_running_out_of == 'coffee':

        #     m 3rksdla "У меня кончился кофе."
            
        # elif items_running_out_of == 'hot chocolate':

        #     m 3rksdla "У меня кончился горячий шоколад."
        ##################
        $ them = "ещё"
        
    if not renpy.seen_label("mas_consumables_refill_explain"):
        call mas_consumables_refill_explain from _call_mas_consumables_refill_explain_2

    $ MAS.MonikaElastic()
    if them == "их":
        m 1eka "Ты ведь не откажешься принести их для меня, правда?"
    else:
        m 1eka "Ты ведь не откажешься принести мне ещё, правда?"


    python:
        for cons in low_cons:
            cons.flagRestockWarn()
    return

label mas_consumables_remove_thermos:

    if not monika_chr.is_wearing_acs_type("thermos-mug"):
        return

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "Я собираюсь убрать эту термокружку. Скоро вернусь.{w=1}{nw}"
    else:

        m 1eua "Подожди секунду, [player], я собираюсь убрать эту термокружку."

    $ thermos = monika_chr.get_acs_of_type("thermos-mug")
    window hide
    call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_4

    python:
        renpy.pause(3.0, hard=True)

        monika_chr.remove_acs(thermos)
        renpy.pause(2.0, hard=True)

    call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_8
    window auto

    $ MAS.MonikaElastic()
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1hua "Я тут!{w=1.5}{nw}"
    else:

        m "Ладно, какие у нас ещё планы на сегодня?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_consumables_candycane_finish_having",
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label mas_consumables_candycane_finish_having:

    python:
        candycane = mas_getConsumable("candycane")
        candycane.acs.keep_on_desk = False
        get_more = candycane.shouldHave() and candycane.hasServing()

    if not get_more:

        python:

            MASConsumable._reset(candycane.consumable_type)
            candycane.acs.keep_on_desk = True

            candycane.done_cons_until = datetime.datetime.now() + MASConsumable.DEF_DONE_CONS_TD
    else:

        if not store.mas_globals.in_idle_mode and (not mas_canCheckActiveWindow() or mas_isFocused()):
            m 1eua "Я собираюсь взять ещё сахарные тросточки."
            m 3eua "Секунду."

        elif store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1esd "О, я съела свои сахарные тросточки.{w=1}{nw}"
            m 1eua "Я собираюсь взять ещё. Я сейчас вернусь.{w=1}{nw}"


        call mas_transition_to_emptydesk from _call_mas_transition_to_emptydesk_5


        python:
            renpy.pause(1.0, hard=True)

            candycane.have()
            candycane.re_serve()

            candycane.use()

            renpy.pause(4.0, hard=True)

        call mas_transition_from_emptydesk ("monika 1eua") from _call_mas_transition_from_emptydesk_9
        $ candycane.acs.keep_on_desk = True

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1hua "Я тут!{w=1.5}{nw}"

            if (
                not mas_inEVL("mas_consumables_generic_queued_running_out")
                and mas_getEV("mas_consumables_generic_queued_running_out").timePassedSinceLastSeen_d(datetime.timedelta(days=7))
                and len(MASConsumable._getLowCons()) > 0
            ):
                $ queueEvent("mas_consumables_generic_queued_running_out")
        else:

            m 1eua "Ладно, чем хочешь заняться сегодня?"
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc

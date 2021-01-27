














init -2 python in mas_sprites:



    import store

    temp_storage = dict()








    _hair__testing_entry = False
    _hair__testing_exit = False
    _clothes__testing_entry = False
    _clothes__testing_exit = False
    _acs__testing_entry = False
    _acs__testing_exit = False





    def _acs_wear_if_found(_moni_chr, acs_name):
        """
        Wears the acs if the acs exists

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory
        """
        acs_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_wear is not None:
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_gifted(_moni_chr, acs_name):
        """
        Wears the acs if it exists and has been gifted/reacted.
        It has been gifted/reacted if the selectable is unlocked.

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory
        """
        acs_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_wear is not None and store.mas_SELisUnlocked(acs_to_wear):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_in_tempstorage(_moni_chr, key):
        """
        Wears the acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage
        """
        acs_items = temp_storage.get(key, None)
        if acs_items is not None:
            for acs_item in acs_items:
                _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_in_tempstorage_s(_moni_chr, key):
        """
        Wears a single acs in tempstorage at the given key, if any.

        IN:
            _moni_chr - MASMonika object
            key - key in tempstorage
        """
        acs_item = temp_storage.get(key, None)
        if acs_item is not None:
            _moni_chr.wear_acs(acs_item)


    def _acs_wear_if_wearing_acs(_moni_chr, acs, acs_to_wear):
        """
        Wears the given acs if wearing another acs.

        IN:
            _moni_chr - MASMonika object
            acs - acs to check if wearing
            acs_to_wear - acs to wear if wearing acs
        """
        if _moni_chr.is_wearing_acs(acs):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - acs type to check if wearing
            acs_to_wear - acs to wear if wearing acs type
        """
        if _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_wear_if_not_wearing_type(_moni_chr, acs_type, acs_to_wear):
        """
        Wears the given acs if NOT wearing an acs of the given type.

        IN:
            _moni_chr - MASMonika object
            acs_type - asc type to check if not wearing
            acs_to_wear - acs to wear if not wearing acs type
        """
        if not _moni_chr.is_wearing_acs_type(acs_type):
            _moni_chr.wear_acs(acs_to_wear)


    def _acs_remove_if_found(_moni_chr, acs_name):
        """
        REmoves an acs if the name exists

        IN:
            _moni_chr - MASMonika object
            acs_name - name of the accessory to remove
        """
        acs_to_remove = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_ACS,
            acs_name
        )
        if acs_to_remove is not None:
            _moni_chr.remove_acs(acs_to_remove)


    def _acs_ribbon_save_and_remove(_moni_chr):
        """
        Removes ribbon acs and aves them to temp storage.

        IN:
            _moni_chr - MASMonika object
        """
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        
        
        if prev_ribbon != store.mas_acs_ribbon_blank:
            temp_storage["hair.ribbon"] = prev_ribbon
        
        if prev_ribbon is not None:
            _moni_chr.remove_acs(prev_ribbon)
        
        
        store.mas_lockEVL("monika_ribbon_select", "EVE")


    def _acs_ribbon_like_save_and_remove(_moni_chr):
        """
        Removes ribbon-like acs and saves them to temp storage, if found

        IN:
            _moni_chr - MASMonika object
        """
        prev_ribbon_like = _moni_chr.get_acs_of_exprop("ribbon-like")
        
        if prev_ribbon_like is not None:
            _moni_chr.remove_acs(prev_ribbon_like)
            temp_storage["hair.ribbon"] = prev_ribbon_like


    def _acs_save_and_remove_exprop(_moni_chr, exprop, key, lock_topics):
        """
        Removes acs with given exprop, saving them to temp storage with
        given key.
        Also locks topics with the exprop if desired

        IN:
            _moni_chr - MASMonika object
            exprop - exprop to remove and save acs
            key - key to use for temp storage
            lock_topics - True will lock topics associated with this exprop
                False will not
        """
        acs_items = _moni_chr.get_acs_of_exprop(exprop, get_all=True)
        if len(acs_items) > 0:
            temp_storage[key] = acs_items
            _moni_chr.remove_acs_exprop(exprop)
        
        if lock_topics:
            lock_exprop_topics(exprop)


    def _hair_unlock_select_if_needed():
        """
        Unlocks the hairdown selector if enough hair is unlocked.
        """
        if len(store.mas_selspr.filter_hair(True)) > 1:
            store.mas_unlockEVL("monika_hair_select", "EVE")


    def _clothes_baked_entry(_moni_chr):
        """
        Clothes baked entry
        """
        for prompt_key in store.mas_selspr.PROMPT_MAP:
            if prompt_key != "clothes":
                prompt_ev = store.mas_selspr.PROMPT_MAP[prompt_key].get(
                    "_ev",
                    None
                )
                if prompt_ev is not None:
                    store.mas_lockEVL(prompt_ev, "EVE")
        
        
        _moni_chr.remove_all_acs()
        
        store.mas_selspr._switch_to_wear_prompts()









    def _hair_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for ponytail
        """
        pass


    def _hair_def_exit(_moni_chr, **kwargs):
        """
        Exit programming point for ponytail
        """
        pass


    def _hair_down_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair down
        """
        pass


    def _hair_down_exit(_moni_chr, **kwargs):
        """
        Exit programming point for hair down
        """
        pass


    def _hair_bun_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair bun
        """
        pass


    def _hair_orcaramelo_bunbraid_exit(_moni_chr, **kwargs):
        """
        Exit prog point for bunbraid
        """

        _moni_chr.remove_acs(store.orcaramelo_sakuya_izayoi_headband)
    
    def _hair_braided_entry(_moni_chr, **kwargs):
        """
        Entry prog point for braided hair
        """
        _moni_chr.wear_acs(store.mas_acs_rin_bows_back)
        _moni_chr.wear_acs(store.mas_acs_rin_bows_front)

    def _hair_braided_exit(_moni_chr, **kwargs):
        """
        Exit prog point for braided hair
        """
        _moni_chr.remove_acs(store.mas_acs_rin_bows_front)
        _moni_chr.remove_acs(store.mas_acs_rin_bows_back)
        
        _moni_chr.remove_acs(store.mas_acs_rin_ears)









    def _clothes_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for def clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            _moni_chr.change_hair(store.mas_hair_def)
            _moni_chr.wear_acs(store.mas_acs_ribbon_def)
        
        store.mas_lockEVL("mas_compliment_outfit", "CMP")

    def _clothes_def_exit(_moni_chr, **kwargs):
        """
        Exit programming point for def clothes
        """
        
        store.mas_unlockEVL("mas_compliment_outfit", "CMP")



    def _clothes_rin_entry(_moni_chr, **kwargs):
        """
        Entry programming point for rin clothes
        """
        outfit_mode = kwargs.get("outfit_mode")
        
        if outfit_mode:
            _moni_chr.change_hair(store.mas_hair_braided)
            _moni_chr.wear_acs(store.mas_acs_rin_ears)


    def _clothes_rin_exit(_moni_chr, **kwargs):
        """
        Exit programming point for rin clothes
        """
        _moni_chr.remove_acs(store.mas_acs_rin_ears)



    def _clothes_marisa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for marisa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.change_hair(store.mas_hair_downtiedstrand)
            _moni_chr.wear_acs(store.mas_acs_marisa_strandbow)
            _moni_chr.wear_acs(store.mas_acs_marisa_witchhat)


    def _clothes_marisa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for marisa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        _moni_chr.remove_acs(store.mas_acs_marisa_strandbow)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_marisa_witchhat)


    def _clothes_orcaramelo_hatsune_miku_entry(_moni_chr, **kwargs):
        """
        Entry pp for orcaramelo miku
        """
        outfit_mode = kwargs.get("outfit_mode", False)

        if outfit_mode:


            _moni_chr.change_hair(store.mas_hair_orcaramelo_twintails)
            _moni_chr.wear_acs(store.mas_acs_orcaramelo_hatsune_miku_headset)
            _moni_chr.wear_acs(
                store.mas_acs_orcaramelo_hatsune_miku_twinsquares
            )


    def _clothes_orcaramelo_hatsune_miku_exit(_moni_chr, **kwargs):
        """
        Exit pp for orcaramelo miku
        """


        _moni_chr.remove_acs(store.mas_acs_orcaramelo_hatsune_miku_headset)
        _moni_chr.remove_acs(store.mas_acs_orcaramelo_hatsune_miku_twinsquares)


    def _clothes_orcaramelo_sakuya_izayoi_entry(_moni_chr, **kwargs):
        """
        Entry pp for orcaramelo sakuya
        """
        outfit_mode = kwargs.get("outfit_mode", False)

        if outfit_mode:


            _moni_chr.change_hair(store.mas_hair_bunbraid)
            _moni_chr.wear_acs(store.orcaramelo_sakuya_izayoi_headband)
            _moni_chr.wear_acs(
                store.orcaramelo_sakuya_izayoi_strandbow
            )


    def _clothes_orcaramelo_sakuya_izayoi_exit(_moni_chr, **kwargs):
        """
        Exit pp for orcaramelo sakuya
        """


        _moni_chr.remove_acs(store.orcaramelo_sakuya_izayoi_headband)
        _moni_chr.remove_acs(store.orcaramelo_sakuya_izayoi_strandbow)


    def _clothes_santa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa clothes
        """
        store.mas_selspr.unlock_acs(store.mas_acs_holly_hairclip)
        
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.change_hair(store.mas_hair_def)
            _moni_chr.wear_acs(store.mas_acs_ribbon_wine)
            _moni_chr.wear_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa clothes
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_lingerie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa lingerie
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.wear_acs(store.mas_acs_holly_hairclip)


    def _clothes_santa_lingerie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa lingerie
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.remove_acs(store.mas_acs_holly_hairclip)


    def _clothes_dress_newyears_entry(_moni_chr, **kwargs):
        """
        entry progpoint for dress_newyears
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            ponytailbraid = store.mas_sprites.get_sprite(
                store.mas_sprites.SP_HAIR,
                "orcaramelo_ponytailbraid"
            )
            if ponytailbraid is not None:
                _moni_chr.change_hair(ponytailbraid)
            
            _moni_chr.wear_acs(store.mas_acs_flower_crown)
            _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
            
            
            hairclip = _moni_chr.get_acs_of_type("left-hair-clip")
            if hairclip:
                _moni_chr.remove_acs(hairclip)
            
            
            ribbon = _moni_chr.get_acs_of_type("ribbon")
            if ribbon:
                _moni_chr.remove_acs(ribbon)


    def _clothes_dress_newyears_exit(_moni_chr, **kwargs):
        """
        exit progpoint for dress_newyears
        """
        _moni_chr.remove_acs(store.mas_acs_flower_crown)
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)

    def _clothes_sundress_white_entry(_moni_chr, **kwargs):
        """
        Entry programming point for sundress white
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
            _moni_chr.wear_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_sundress_white_exit(_moni_chr, **kwargs):
        """
        Exit programming point for sundress white
        """
        
        
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.remove_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_velius94_dress_whitenavyblue_entry(_moni_chr, **kwargs):
        """
        Entry prog point for navyblue dress
        """
        outfit_mode = kwargs.get("outfit_mode", False)
        
        if outfit_mode:
            
            if (
                    not _moni_chr.is_wearing_hair_with_exprop("ribbon")
                    or _moni_chr.is_wearing_hair_with_exprop("twintails")
            ):
                _moni_chr.change_hair(store.mas_hair_def)
            
            _acs_wear_if_gifted(_moni_chr, "velius94_bunnyscrunchie_blue")






    def _acs_quetzalplushie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie acs
        """
        
        store.mas_showEVL('monika_plushie', 'EVE', _random=True)
        
        if store.persistent._mas_d25_deco_active:
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie_santahat)


    def _acs_quetzalplushie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for quetzal plushie acs
        """
        
        store.mas_hideEVL('monika_plushie', 'EVE', derandom=True)
        
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_santahat)
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_antlers)
    
    def _acs_center_quetzalplushie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie (mid version) acs
        """
        store.mas_showEVL("monika_plushie", "EVE", _random=True)
        
        if store.persistent._mas_d25_deco_active:
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie_center_santahat)

    def _acs_center_quetzalplushie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for quetzal plushie (mid version) acs
        """
        store.mas_hideEVL("monika_plushie", "EVE", derandom=True)
        
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_center_santahat)


    def _acs_quetzalplushie_santahat_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie santa hat acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)
    
    def _acs_center_quetzalplushie_santahat_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie santa hat (mid version) acs
        """
        _moni_chr.wear_acs(store.mas_acs_center_quetzalplushie)


    def _acs_quetzalplushie_antlers_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie antlers acs
        """
        
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_entry(_moni_chr, **kwargs):
        """
        Entry programming point for heartchoc acs
        """
        
        
        
        
        
        
        if not (store.mas_isF14() or store.mas_isD25Season()):
            if _moni_chr.is_wearing_acs(store.mas_acs_quetzalplushie):
                _moni_chr.wear_acs(store.mas_acs_center_quetzalplushie)
        
        else:
            _moni_chr.remove_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_exit(_moni_chr, **kwargs):
        """
        Exit programming point for heartchoc acs
        """
        if _moni_chr.is_wearing_acs(store.mas_acs_center_quetzalplushie):
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie)

init -1 python:








































    mas_hair_def = MASHair(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),


        ex_props={
            "ribbon": True,
            "ribbon-restore": True
        }
    )
    store.mas_sprites.init_hair(mas_hair_def)
    store.mas_selspr.init_selectable_hair(
        mas_hair_def,
        "Хвостик",
        "def",
        "hair",
        select_dlg=[
            "Тебе нравится моя косичка, [player]?"
        ]
    )
    store.mas_selspr.unlock_hair(mas_hair_def)





    mas_hair_down = MASHair(
        "down",
        "down",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        ex_props={
            store.mas_sprites.EXP_H_NT: True,
        }



    )
    store.mas_sprites.init_hair(mas_hair_down)
    store.mas_selspr.init_selectable_hair(
        mas_hair_down,
        "Распущенные волосы",
        "down",
        "hair",
        select_dlg=[
            "Как же приятно распустить свои волосы..."
        ]
    )





    mas_hair_downtiedstrand = MASHair(
        "downtiedstrand",
        "downtiedstrand",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        ex_props={
            store.mas_sprites.EXP_H_RQCP: store.mas_sprites.EXP_C_BRS,
            store.mas_sprites.EXP_H_TS: True,
            store.mas_sprites.EXP_H_NT: True,
        }
    )
    store.mas_sprites.init_hair(mas_hair_downtiedstrand)
    store.mas_selspr.init_selectable_hair(
        mas_hair_downtiedstrand,
        "Распущенные волосы с хвостиком",
        "downtiedstrand",
        "hair",
        select_dlg=[
            "Как же приятно распустить свои волосы...",
            "Выглядит мило, тебе не кажется?"
        ]
    )

    mas_hair_braided = MASHair(
        "braided",
        "braided",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        ex_props={
            store.mas_sprites.EXP_H_TB: True,
            store.mas_sprites.EXP_H_RQCP: "rin"
        },
        entry_pp=store.mas_sprites._hair_braided_entry,
        exit_pp=store.mas_sprites._hair_braided_exit
    )
    store.mas_sprites.init_hair(mas_hair_braided)
    store.mas_selspr.init_selectable_hair(
        mas_hair_braided,
        "Заплетенная причёска",
        "braided",
        "hair",
        select_dlg=[
            "Выглядит мило, тебе не кажется?"
        ]
    )

    mas_hair_ponytail = MASHair(
        "ponytail",
        "def",
        MASPoseMap(
            default = True,
            use_reg_for_l=True,
        ),

        ex_props={
            "ribbon": True,
            "ribbon-off": True,
        }
    )


    mas_hair_bun = MASHair(
        "bun",
        "bun",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_bun)
    store.mas_selspr.init_selectable_hair(
        mas_hair_bun,
        "Пучок",
        "bun",
        "hair",
    )


    mas_hair_ponytailbraid = MASHair(
        "orcaramelo_ponytailbraid",
        "orcaramelo_ponytailbraid",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_ponytailbraid)

    store.mas_selspr.init_selectable_hair(
        mas_hair_ponytailbraid,
        "Хвостик с косичкой",
        "orcaramelo_ponytailbraid",
        "hair",
    )

    mas_hair_twinbun = MASHair(
        "orcaramelo_twinbun",
        "orcaramelo_twinbun",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_twinbun)

    store.mas_selspr.init_selectable_hair(
        mas_hair_twinbun,
        "Два пучка",
        "orcaramelo_twinbun",
        "hair",
    )

    mas_hair_bunbraid = MASHair(
        "orcaramelo_bunbraid",
        "orcaramelo_bunbraid",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
            "braidstrand": True,
            "bunbraid": True
        }
    )

    store.mas_sprites.init_hair(mas_hair_bunbraid)

    store.mas_selspr.init_selectable_hair(
        mas_hair_bunbraid,
        "Пучок с косичкой",
        "orcaramelo_bunbraid",
        "hair",
    )

    # mas_hair_twintails = MASHair(
    #     "orcaramelo_twintails",
    #     "orcaramelo_twintails",
    #     MASPoseMap(
    #         mpm_type=0,
    #         default=True,
    #         use_reg_for_l=True
    #     ),
    #
    #
    #     stay_on_start=True,
    #     ex_props={
    #         "ribbon": True,
    #     }
    # )
    #
    # store.mas_sprites.init_hair(mas_hair_twintails)
    #
    # store.mas_selspr.init_selectable_hair(
    #     mas_hair_twintails,
    #     "Два хвостика",
    #     "orcaramelo_twintails",
    #     "hair",
    # )
    mas_hair_orcaramelo_twintails = MASHair(
        "orcaramelo_twintails",
        "orcaramelo_twintails",
        MASPoseMap(
            default=True,
            l_default=True
        ),
        ex_props={
            "ribbon": True,
            "twintails": True,
        }
    )
    store.mas_sprites.init_hair(mas_hair_orcaramelo_twintails)
    store.mas_selspr.init_selectable_hair(
        mas_hair_orcaramelo_twintails,
        "Два хвостика",
        "orcaramelo_twintails",
        "hair",
        visible_when_locked=False
    )

    mas_hair_usagi = MASHair(
        "orcaramelo_usagi",
        "orcaramelo_usagi",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_usagi)

    store.mas_selspr.init_selectable_hair(
        mas_hair_usagi,
        "Усаги",
        "orcaramelo_usagi",
        "hair",
    )

    mas_hair_downshort = MASHair(
        "echo_downshort",
        "echo_downshort",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "no-tails": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_downshort)

    store.mas_selspr.init_selectable_hair(
        mas_hair_downshort,
        "Короткие распущенные волосы",
        "echo_downshort",
        "hair",
    )

    mas_hair_ponytailshort = MASHair(
        "echo_ponytailshort",
        "echo_ponytailshort",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),


        stay_on_start=True,
        ex_props={
            "ribbon": True,
        }
    )

    store.mas_sprites.init_hair(mas_hair_ponytailshort)

    store.mas_selspr.init_selectable_hair(
        mas_hair_ponytailshort,
        "Короткие волосы с хвостиком",
        "echo_ponytailshort",
        "hair",
    )


    mas_hair_custom = MASHair(
        "custom",
        "custom",
        MASPoseMap(),

        
        split=MASPoseMap(
            default=False,
            use_reg_for_l=True
        ),
    )
    store.mas_sprites.init_hair(mas_hair_custom)


init -1 python:




























    mas_clothes_def = MASClothes(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_def_entry,
        exit_pp=store.mas_sprites._clothes_def_exit
    )
    store.mas_sprites.init_clothes(mas_clothes_def)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_def,
        "Школьная форма",
        "schooluniform",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Готова к школе!"
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)






    mas_clothes_blackdress = MASClothes(
        "blackdress",
        "blackdress",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_blackdress)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_blackdress,
        "Чёрное платье",
        "blackdress",
        "clothes",
        visible_when_locked=False,
        select_dlg=[
            "Мы идём в какое-то особенное место, [player]?"
        ]
    )






    mas_clothes_blazerless = MASClothes(
        "blazerless",
        "blazerless",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True
        },
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        )
    )
    store.mas_sprites.init_clothes(mas_clothes_blazerless)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_blazerless,
        "Школьная форма без пиджака",
        "schooluniform_blazerless",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Ах, как хорошо без пиджака!",
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)


    mas_clothes_shirt_blue = MASClothes(
        "finale_shirt_blue",
        "finale_shirt_blue",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True,
        ),
        stay_on_start=True,
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                2: MASArmLeft(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                3: MASArmLeft(
                    "rest",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                4: MASArmRight(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                5: MASArmRight(
                    "point",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                6: MASArmRight(
                    "restpoint",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                7: MASArmBoth(
                    "steepling",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                8: MASArmLeft(
                    "def",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
    )
    store.mas_sprites.init_clothes(mas_clothes_shirt_blue)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_shirt_blue,
        "Синяя футболка",
        "finale_shirt_blue",
        "clothes",
        hover_dlg=None,
        select_dlg=[
            "Отличный выбор, [player]! Мне в ней очень комфортно~",
        ]
    )

    mas_clothes_bikini_shell = MASClothes(
        "orcaramelo_bikini_shell",
        "orcaramelo_bikini_shell",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        pose_arms=MASPoseArms({}, def_base=False)
    )

    store.mas_sprites.init_clothes(mas_clothes_bikini_shell)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_bikini_shell,
        "Бикини с ракушками",
        "orcaramelo_bikini_shell",
        "clothes",
        select_dlg=[
            "Ракушки ракушки, на берегу моря~",
            "Кто сказал, что русалки не настоящие?"
        ]
    )

    mas_clothes_shirt_pink = MASClothes(
        "velius94_shirt_pink",
        "velius94_shirt_pink",
        MASPoseMap(
            mpm_type=0,
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            "bare-right-shoulder": True,
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )

    store.mas_sprites.init_clothes(mas_clothes_shirt_pink)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_shirt_pink,
        "Сарафан (Розовый)",
        "velius94_shirt_pink",
        "clothes",
        select_dlg=[
            "Красивая в розовом~"
        ]
    )



    mas_clothes_marisa = MASClothes(
        "marisa",
        "marisa",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_marisa_entry,
        exit_pp=store.mas_sprites._clothes_marisa_exit,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
            store.mas_sprites.EXP_C_COST: "o31",
            store.mas_sprites.EXP_C_COSP: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_marisa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_marisa,
        "Костюм ведьмы",
        "marisa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Просто обычный костюм, хех~"
        ]
    )

    mas_clothes_rin = MASClothes(
        "rin",
        "rin",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_rin_entry,
        exit_pp=store.mas_sprites._clothes_rin_exit,
        ex_props={
            store.mas_sprites.EXP_C_COST: "o31",
            store.mas_sprites.EXP_C_COSP: True,
            "rin": True 
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_rin)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_rin,
        "Костюм кошки",
        "rin",
        "clothes",
        visible_when_locked=False,
        hover_dlg=[
            "~ня?",
            "ня-я..."
        ],
        select_dlg=[
            "Ня!"
        ]
    )






















































    mas_clothes_santa = MASClothes(
        "santa",
        "santa",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_santa_entry,
        exit_pp=store.mas_sprites._clothes_santa_exit,
        ex_props={
            "costume": "d25"
        },
    )
    store.mas_sprites.init_clothes(mas_clothes_santa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa,
        "Костюм Санты",
        "santa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Счастливого Рождества!",
            "Какие {i}подарки{/i} ты хочешь?",
            "Счастливых праздников!"
        ]
    )





    mas_clothes_santa_lingerie = MASClothes(
        "santa_lingerie",
        "santa_lingerie",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
            "lingerie": "d25"
        },
        entry_pp=store.mas_sprites._clothes_santa_lingerie_entry,
        exit_pp=store.mas_sprites._clothes_santa_lingerie_exit,
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_santa_lingerie)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa_lingerie,
        "Нижнее бельё Санты",
        "santa_lingerie",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Хочешь открыть свой подарок?~",
            "Какие {i}подарки{/i} ты хочешь?",
            "Открой свой подарок, э-хе-хе~",
            "Всё, что я хочу на Рождество - это ты~",
            "Санта, детка~",
            "Что {i}ещё{/i} ты хочешь развернуть?~"
        ]
    )






    mas_clothes_dress_newyears = MASClothes(
        "new_years_dress",
        "new_years_dress",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        entry_pp=store.mas_sprites._clothes_dress_newyears_entry,
        exit_pp=store.mas_sprites._clothes_dress_newyears_exit,
        stay_on_start=True,
        pose_arms=MASPoseArms({}, def_base=False),
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_dress_newyears)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_dress_newyears,
        "Новогоднее платье",
        "new_years_dress",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Мы идём в какое-то особенное место, [player]?",
            "Очень официально!",
            "Любой особый случай, [player]?"
        ],
    )





    mas_clothes_sundress_white = MASClothes(
        "sundress_white",
        "sundress_white",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_sundress_white_entry,
        exit_pp=store.mas_sprites._clothes_sundress_white_exit,
        pose_arms=MASPoseArms({}, def_base=False),
        ex_props={
            store.mas_sprites.EXP_C_BRS: True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_sundress_white)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_sundress_white,
        "Сарафан (белый)",
        "sundress_white",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Мы сегодня идём в какое-то особенное место, [player]?",
            "Мне всегда нравилась эта одежда...",
        ],
    )





    mas_clothes_vday_lingerie = MASClothes(
        "vday_lingerie",
        "vday_lingerie",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
            store.mas_sprites.EXP_C_BRS: True
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_vday_lingerie)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_vday_lingerie,
        "Нижнее бельё с розовой тесьмой",
        "vday_lingerie",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Э-хе-хе~",
            "Тебе нравится, [player]?"
        ]
    )

    finale_jacket_brown = MASClothes(
        "finale_jacket_brown",
        "finale_jacket_brown",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                2: MASArmLeft(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                3: MASArmLeft(
                    "rest",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                4: MASArmRight(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                5: MASArmRight(
                    "point",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                6: MASArmRight(
                    "restpoint",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                7: MASArmBoth(
                    "steepling",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                8: MASArmLeft(
                    "def",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
    )
    store.mas_sprites.init_clothes(finale_jacket_brown)
    store.mas_selspr.init_selectable_clothes(
        finale_jacket_brown,
        "Коричневое пальто",
        "finale_jacket_brown",
        "clothes",
        select_dlg=[
            "Приятно и тепло~",
            "Мы куда-то идём, [player]?"
        ]
    )

    finale_hoodie_green = MASClothes(
        "finale_hoodie_green",
        "finale_hoodie_green",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
        # pose_arms=MASPoseArms(
        #     {
        #         1: MASArmBoth(
        #             "crossed",
        #             {
        #                 MASArm.LAYER_MID: True,
        #             }
        #         ),
        #         2: MASArmLeft(
        #             "down",
        #             {
        #                 MASArm.LAYER_BOT: True,
        #             }
        #         ),
        #         3: MASArmLeft(
        #             "rest",
        #             {
        #                 MASArm.LAYER_TOP: True,
        #             }
        #         ),
        #         4: MASArmRight(
        #             "down",
        #             {
        #                 MASArm.LAYER_BOT: True,
        #             }
        #         ),
        #         5: MASArmRight(
        #             "point",
        #             {
        #                 MASArm.LAYER_BOT: True,
        #             }
        #         ),
        #         6: MASArmRight(
        #             "restpoint",
        #             {
        #                 MASArm.LAYER_TOP: True,
        #             }
        #         ),
        #         7: MASArmBoth(
        #             "steepling",
        #             {
        #                 MASArm.LAYER_TOP: True,
        #             }
        #         ),
        #         8: MASArmLeft(
        #             "def",
        #             {
        #                 MASArm.LAYER_TOP: True,
        #             }
        #         ),
        #         9: MASArmRight(
        #             "def",
        #             {
        #                 MASArm.LAYER_MID: True,
        #             }
        #         ),
        #     }
        # ),
    )
    store.mas_sprites.init_clothes(finale_hoodie_green)
    store.mas_selspr.init_selectable_clothes(
        finale_hoodie_green,
        "Зелёное худи",
        "finale_hoodie_green",
        "clothes",
        select_dlg=[
            "Нет ничего более удобного, чем худи!"
        ]
    )

    mocca_bun_blackandwhitestripedpullover = MASClothes(
        "mocca_bun_blackandwhitestripedpullover",
        "mocca_bun_blackandwhitestripedpullover",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
        ex_props={
            "bare-right-shoulder": True,
        },
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                2: MASArmLeft(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                3: MASArmLeft(
                    "rest",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                4: MASArmRight(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                5: MASArmRight(
                    "point",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                6: MASArmRight(
                    "restpoint",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                7: MASArmBoth(
                    "steepling",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                8: MASArmLeft(
                    "def",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
    )
    store.mas_sprites.init_clothes(mocca_bun_blackandwhitestripedpullover)
    store.mas_selspr.init_selectable_clothes(
        mocca_bun_blackandwhitestripedpullover,
        "Свитер с чёрно-белыми линиями",
        "mocca_bun_blackandwhitestripedpullover",
        "clothes",
        select_dlg=[
            "Как я выгляжу, [player]?",
            "Очень мило, не так ли?",
            "Хороший выбор, [player]! Это так удобно~"
        ]
    )

    orcaramelo_sweater_shoulderless = MASClothes(
        "orcaramelo_sweater_shoulderless",
        "orcaramelo_sweater_shoulderless",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless)
    store.mas_selspr.init_selectable_clothes(
        orcaramelo_sweater_shoulderless,
        "Свитер без плеч",
        "orcaramelo_sweater_shoulderless",
        "clothes",
        select_dlg=[
            "Чувствую себя уютно~",
            "Подходит для зимнего дня!",
            "Очень тепло..."
        ]
    )

    orcaramelo_sweater_shoulderless_red = MASClothes(
        "orcaramelo_sweater_shoulderless_red",
        "orcaramelo_sweater_shoulderless_red",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_red)

    orcaramelo_sweater_shoulderless_orange = MASClothes(
        "orcaramelo_sweater_shoulderless_orange",
        "orcaramelo_sweater_shoulderless_orange",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_orange)

    orcaramelo_sweater_shoulderless_green = MASClothes(
        "orcaramelo_sweater_shoulderless_green",
        "orcaramelo_sweater_shoulderless_green",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_green)

    orcaramelo_sweater_shoulderless_blue = MASClothes(
        "orcaramelo_sweater_shoulderless_blue",
        "orcaramelo_sweater_shoulderless_blue",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_blue)

    orcaramelo_sweater_shoulderless_darkblue = MASClothes(
        "orcaramelo_sweater_shoulderless_darkblue",
        "orcaramelo_sweater_shoulderless_darkblue",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_darkblue)

    orcaramelo_sweater_shoulderless_purple = MASClothes(
        "orcaramelo_sweater_shoulderless_purple",
        "orcaramelo_sweater_shoulderless_purple",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_purple)

    orcaramelo_sweater_shoulderless_pink = MASClothes(
        "orcaramelo_sweater_shoulderless_pink",
        "orcaramelo_sweater_shoulderless_pink",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
    )
    store.mas_sprites.init_clothes(orcaramelo_sweater_shoulderless_pink)

    velius94_dress_whitenavyblue = MASClothes(
        "velius94_dress_whitenavyblue",
        "velius94_dress_whitenavyblue",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_velius94_dress_whitenavyblue_entry,
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                2: MASArmLeft(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                3: MASArmLeft(
                    "rest",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                4: MASArmRight(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                5: MASArmRight(
                    "point",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                6: MASArmRight(
                    "restpoint",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                7: MASArmBoth(
                    "steepling",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                8: MASArmLeft(
                    "def",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
    )
    store.mas_sprites.init_clothes(velius94_dress_whitenavyblue)
    store.mas_selspr.init_selectable_clothes(
        velius94_dress_whitenavyblue,
        "Белое и тёмно-синее платье",
        "velius94_dress_whitenavyblue",
        "clothes",
    )

init -1 python:





















    mas_acs_candycane = MASAccessory(
        "candycane",
        "candycane",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="plate",
        mux_type=store.mas_sprites.DEF_MUX_LD,
        keep_on_desk=False
    )
    store.mas_sprites.init_acs(mas_acs_candycane)





    mas_acs_christmascookies = MASAccessory(
        "christmas_cookies",
        "christmas_cookies",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="plate",
        mux_type=store.mas_sprites.DEF_MUX_LD,
        keep_on_desk=False
    )
    store.mas_sprites.init_acs(mas_acs_christmascookies)







    mas_acs_mug = MASAccessory(
        "mug",
        "mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"],
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_mug)





    mas_acs_thermos_mug = MASAccessory(
        "thermos_mug",
        "thermos_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="thermos-mug"
    )
    store.mas_sprites.init_acs(mas_acs_thermos_mug)
    store.mas_selspr.init_selectable_acs(
        mas_acs_thermos_mug,
        "Термокружка «Только Моника»",
        "thermos_justmonika",
        "thermos-mug"
    )


    jmo_hairclip_cherry = MASAccessory(
        "jmo_hairclip_cherry",
        "jmo_hairclip_cherry",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(jmo_hairclip_cherry)

    store.mas_selspr.init_selectable_acs(
        jmo_hairclip_cherry,
        "Заколка с вишенкой",
        "jmo_hairclip_cherry",
        "left-hair-clip",
        hover_dlg=[
            "Слышал[mas_gender_none] ли ты о вишнёвом поцелуе, [player]?~"
        ],
        select_dlg=[
            "Мне нравится эта заколка.",
            "Эта заколка восхитительна!",
            "Мило!"
        ]
    )

    jmo_hairclip_heart = MASAccessory(
        "jmo_hairclip_heart",
        "jmo_hairclip_heart",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(jmo_hairclip_heart)

    store.mas_selspr.init_selectable_acs(
        jmo_hairclip_heart,
        "Заколка с сердечком",
        "jmo_hairclip_heart",
        "left-hair-clip",
        hover_dlg=[
            "Немного любви..."
        ],
        select_dlg=[
            "Мне нравится эта заколка.",
            "Эта заколка восхитительна!",
            "Мило!"
        ]
    )

    bellmandi86_hairclip_crescentmoon = MASAccessory(
        "bellmandi86_hairclip_crescentmoon",
        "bellmandi86_hairclip_crescentmoon",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(bellmandi86_hairclip_crescentmoon)

    store.mas_selspr.init_selectable_acs(
        bellmandi86_hairclip_crescentmoon,
        "Заколка с полумесяцем",
        "bellmandi86_hairclip_crescentmoon",
        "left-hair-clip",
        select_dlg=[
            "С тех пор как я встретила тебя, я была на седьмом небе от счастья!",
            "Я люблю тебя до луны и обратно~",
            "Наступает ночь...",
            "Полетели со мной на луну!"
        ]
    )

    bellmandi86_hairclip_ghost = MASAccessory(
        "bellmandi86_hairclip_ghost",
        "bellmandi86_hairclip_ghost",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(bellmandi86_hairclip_ghost)

    store.mas_selspr.init_selectable_acs(
        bellmandi86_hairclip_ghost,
        "Заколка с призраком",
        "bellmandi86_hairclip_ghost",
        "left-hair-clip",
        select_dlg=[
            "Стра-а-а-а-а-а-ашно!",
            "БУ-У!",
            "Кому ты собираешься звонить?",
            "Я не боюсь никаких призраков.",
            "Если в твоём районе есть что-то странное..."
        ]
    )

    bellmandi86_hairclip_pumpkin = MASAccessory(
        "bellmandi86_hairclip_pumpkin",
        "bellmandi86_hairclip_pumpkin",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(bellmandi86_hairclip_pumpkin)

    store.mas_selspr.init_selectable_acs(
        bellmandi86_hairclip_pumpkin,
        "Заколка с тыковкой",
        "bellmandi86_hairclip_pumpkin",
        "left-hair-clip",
        select_dlg=[
            "Что получится, если разделить окружность тыквы на её диаметр? Тыквенное Пи!",
            "Биббиди-боббиди-бу!",
            "Интересно, раньше это была карета?..",
            "Это отличная тыква, [player]!",
            "Это так мило, моя маленькая тыква~"
        ]
    )

    bellmandi86_hairclip_bat = MASAccessory(
        "bellmandi86_hairclip_bat",
        "bellmandi86_hairclip_bat",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(bellmandi86_hairclip_bat)

    store.mas_selspr.init_selectable_acs(
        bellmandi86_hairclip_bat,
        "Заколка с летучей мышью",
        "bellmandi86_hairclip_bat",
        "left-hair-clip",
        select_dlg=[
            "Летучая мышь в моих волосах? Это самый страшный кошмар для многих людей!",
            "Надеюсь, у тебя нет хироптофобии, [player]~",
            "Надеюсь, она не запуталась!"
        ]
    )

    jmo_hairclip_musicnote = MASAccessory(
        "jmo_hairclip_musicnote",
        "jmo_hairclip_musicnote",
        MASPoseMap(
            default="0",
            p5="5",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        mux_type=["left-hair-clip"],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        rec_layer=5,
    )
    store.mas_sprites.init_acs(jmo_hairclip_musicnote)

    store.mas_selspr.init_selectable_acs(
        jmo_hairclip_musicnote,
        "Заколка с восьмой нотой",
        "jmo_hairclip_musicnote",
        "left-hair-clip",
        hover_dlg=[
            "{i}Каждый день~{/i}"
        ],
        select_dlg=[
            "Мне нравится эта заколка.",
            "Эта заколка восхитительна!",
            "Мило!"
        ]
    )



    mas_acs_ear_rose = MASAccessory(
        "ear_rose",
        "ear_rose",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        acs_type="left-hair-flower-ear",
        mux_type=[
            "left-hair-flower-ear",
            "left-hair-flower"
        ],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        priority=20,
        stay_on_start=False,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_ear_rose)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ear_rose,
        "Роза",
        "hairflower_rose",
        "left-hair-flower",
        # hover_dlg=[
        #     "Сказка стара как мир",
        # ],
        # select_dlg=[
        #     "Правда, на",
        # ]
    )



    mas_acs_hairflower_pink = MASAccessory(
        "orcaramelo_hairflower_pink",
        "orcaramelo_hairflower_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        acs_type="left-hair-flower",
        mux_type=[
            "left-hair-flower",
        ],
        ex_props={
            "left-hair-strand-eye-level": True,
        },
        priority=20,
        stay_on_start=False,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_hairflower_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_hairflower_pink,
        "Розовый цветок",
        "orcaramelo_hairflower_pink",
        "left-hair-flower",
    )

    trilasent_choker_flowered = MASSplitAccessory(
        "trilasent_choker_flowered",
        "trilasent_choker_flowered",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        acs_type="choker",
        mux_type=[
            "choker",
        ],
        stay_on_start=True,
        rec_layer=8,
        arm_split=MASPoseMap(
            default="0",
            use_reg_for_l=True
        )
    )
    store.mas_sprites.init_acs(trilasent_choker_flowered)
    store.mas_selspr.init_selectable_acs(
        trilasent_choker_flowered,
        "Цветочный чокер",
        "trilasent_choker_flowered",
        "choker",
    )

    trilasent_choker_simple = MASSplitAccessory(
        "trilasent_choker_simple",
        "trilasent_choker_simple",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        acs_type="choker",
        mux_type=[
            "choker",
        ],
        stay_on_start=True,
        rec_layer=8,
        arm_split=MASPoseMap(
            default="0",
            use_reg_for_l=True
        )
    )
    store.mas_sprites.init_acs(trilasent_choker_simple)
    store.mas_selspr.init_selectable_acs(
        trilasent_choker_simple,
        "Обычный чокер",
        "trilasent_choker_simple",
        "choker",
    )

    sirnimblybottoms_heart_choker = MASSplitAccessory(
        "sirnimblybottoms_heart_choker",
        "sirnimblybottoms_heart_choker",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        acs_type="choker",
        mux_type=[
            "choker",
        ],
        stay_on_start=True,
        rec_layer=8,
        arm_split=MASPoseMap(
            default="0",
            use_reg_for_l=True
        )
    )
    store.mas_sprites.init_acs(sirnimblybottoms_heart_choker)
    store.mas_selspr.init_selectable_acs(
        sirnimblybottoms_heart_choker,
        "Чокер с сердцем",
        "sirnimblybottoms_heart_choker",
        "choker",
    )

    mas_acs_hairties_bracelet_brown = MASSplitAccessory(
        "hairties_bracelet_brown",
        "hairties_bracelet_brown",
        MASPoseMap(
            p1="1",
            p2="2",
            p3="1",
            p4="4",
            p5="5",
            p6=None,
            p7="1"
        ),
        stay_on_start=True,
        acs_type="wrist-bracelet",
        mux_type=["wrist-bracelet"],
        ex_props={
            "bare wrist": True,
        },
        rec_layer=MASMonika.ASE_ACS,
        arm_split=MASPoseMap(
            default="",
            p1="10",
            p2="5",
            p3="10",
            p4="0",
            p5="10",
            p7="10",
        )
    )
    store.mas_sprites.init_acs(mas_acs_hairties_bracelet_brown)





    mas_acs_heartchoc = MASAccessory(
        "heartchoc",
        "heartchoc",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="chocs",
        mux_type=store.mas_sprites.DEF_MUX_LD,
        keep_on_desk=False
    )
    store.mas_sprites.init_acs(mas_acs_heartchoc)





    mas_acs_hotchoc_mug = MASAccessory(
        "hotchoc_mug",
        "hotchoc_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"],
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_hotchoc_mug)





    mas_acs_musicnote_necklace_gold = MASSplitAccessory(
        "musicnote_necklace_gold",
        "musicnote_necklace_gold",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="necklace",
        mux_type=["necklace"],
        ex_props={
            "bare collar": True,
        },
        rec_layer=MASMonika.BSE_ACS,
        arm_split=MASPoseMap(
            default="0",
        )
    )
    store.mas_sprites.init_acs(mas_acs_musicnote_necklace_gold)





    mas_acs_marisa_strandbow = MASAccessory(
        "marisa_strandbow",
        "marisa_strandbow",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="strandbow",
        
        ex_props={
            store.mas_sprites.EXP_A_RQHP: store.mas_sprites.EXP_H_TS,
        },
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_marisa_strandbow)





    mas_acs_marisa_witchhat = MASAccessory(
        "marisa_witchhat",
        "marisa_witchhat",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="hat",
        mux_type=["hat"],
        ex_props={
            store.mas_sprites.EXP_A_RQHP: store.mas_sprites.EXP_H_NT,
            store.mas_sprites.EXP_A_EXCLHP: store.mas_sprites.EXP_H_TB
        },
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_marisa_witchhat)
    store.mas_selspr.init_selectable_acs(
        mas_acs_marisa_witchhat,
        "Колпак ведьмы", 
        "marisa_witchhat",
        "hat",
        select_dlg=[
            "Хе~",
            "Время чая, время чая. Даже если у нас есть кофе, это время чая. Э-хе-хе~",
            "Глаз Тритона, палец лягушки...",
            "И где же я оставила эту метлу?.."
        ]
    )

    mas_acs_rin_bows_front = MASAccessory(
        "rin_bows_front",
        "rin_bows_front",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="ribbon-front",
        mux_type=["ribbon-front"],
        rec_layer=MASMonika.AFH_ACS,
        priority=20
    )
    store.mas_sprites.init_acs(mas_acs_rin_bows_front)





    mas_acs_rin_bows_back = MASAccessory(
        "rin_bows_back",
        "rin_bows_back",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="ribbon-back",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_rin_bows_back)





    mas_acs_rin_ears = MASAccessory(
        "rin_ears",
        "rin_ears",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="headband",
        rec_layer=MASMonika.AFH_ACS,
        priority=5
    )
    store.mas_sprites.init_acs(mas_acs_rin_ears)


    mas_clothes_orcaramelo_hatsune_miku = MASClothes(
        "orcaramelo_hatsune_miku",
        "orcaramelo_hatsune_miku",


        MASPoseMap(
            default=True,
            l_default=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_orcaramelo_hatsune_miku_entry,
        exit_pp=store.mas_sprites._clothes_orcaramelo_hatsune_miku_exit,
        ex_props={
            "desired-hair-prop": "twintails",
            "costume": True,
            "cosplay": True,
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_orcaramelo_hatsune_miku)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_orcaramelo_hatsune_miku,
        "Хацунэ Мику",
        "orcaramelo_hatsune_miku",
        "clothes",
        visible_when_locked=False,
        select_dlg=[
            "Первый звук будущего!",
            "Готова к выходу на сцену!",
            "Не хватает только лука-порея..."
        ]
    )

    mas_acs_orcaramelo_hatsune_miku_headset = MASAccessory(
        "orcaramelo_hatsune_miku_headset",
        "orcaramelo_hatsune_miku_headset",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="headset",

        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_orcaramelo_hatsune_miku_headset)






    mas_acs_orcaramelo_hatsune_miku_twinsquares = MASAccessory(
        "orcaramelo_hatsune_miku_twinsquares",
        "orcaramelo_hatsune_miku_twinsquares",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="twin-ribbons",

        ex_props={
            "twin-ribbon": True,
            "ribbon-like": True,
            "required-hair-prop": "twintails",
        },
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_orcaramelo_hatsune_miku_twinsquares)



    mas_acs_holly_hairclip = MASAccessory(
        "holly_hairclip",
        "holly_hairclip",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="left-hair-clip",
        
        rec_layer=MASMonika.AFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_holly_hairclip)
    store.mas_selspr.init_selectable_acs(
        mas_acs_holly_hairclip,
        "Остролистовая заколка",
        "holly_hairclip",
        "left-hair-clip",
        select_dlg=[
            "Готов украшать залы, [player]?"
        ]
    )





    mas_acs_flower_crown = MASAccessory(
        "flower_crown",
        "flower_crown",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        acs_type="front-hair-flower-crown",
        priority=20,
        stay_on_start=True,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_flower_crown)

    mas_clothes_orcaramelo_sakuya_izayoi = MASClothes(
        "orcaramelo_sakuya_izayoi",
        "orcaramelo_sakuya_izayoi",
        MASPoseMap(
            mpm_type=0,
            default=False,
            use_reg_for_l=True,
            p1=True,
            p2=True,
            p3=True,
            p4=True,
            p5=True,
            p6=True,
            p7=True,
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_orcaramelo_sakuya_izayoi_entry,
        exit_pp=store.mas_sprites._clothes_orcaramelo_sakuya_izayoi_exit,
        pose_arms=MASPoseArms(
            {
                1: MASArmBoth(
                    "crossed",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
                2: MASArmLeft(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                3: MASArmLeft(
                    "rest",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                4: MASArmRight(
                    "down",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                5: MASArmRight(
                    "point",
                    {
                        MASArm.LAYER_BOT: True,
                    }
                ),
                6: MASArmRight(
                    "restpoint",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                7: MASArmBoth(
                    "steepling",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                8: MASArmLeft(
                    "def",
                    {
                        MASArm.LAYER_TOP: True,
                    }
                ),
                9: MASArmRight(
                    "def",
                    {
                        MASArm.LAYER_MID: True,
                    }
                ),
            }
        ),
    )
    store.mas_sprites.init_clothes(mas_clothes_orcaramelo_sakuya_izayoi)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_orcaramelo_sakuya_izayoi,
        "Сакуя Идзаей",
        "orcaramelo_sakuya_izayoi",
        "clothes",
        hover_dlg=None,
        select_dlg=[
            "Время всегда останавливается, когда я с тобой~",
            "Позволь предложить тебе моё гостеприимство.",
            "Не хочешь ли чашечку чая, [player]?"
        ]
    )

    orcaramelo_sakuya_izayoi_strandbow = MASAccessory(
        "orcaramelo_sakuya_izayoi_strandbow",
        "orcaramelo_sakuya_izayoi_strandbow",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="strandbow",

        rec_layer=5
    )
    store.mas_sprites.init_acs(orcaramelo_sakuya_izayoi_strandbow)

    orcaramelo_sakuya_izayoi_headband = MASAccessory(
        "orcaramelo_sakuya_izayoi_headband",
        "orcaramelo_sakuya_izayoi_headband",
        MASPoseMap(
            default="0",
            l_default="5"
        ),
        stay_on_start=True,
        acs_type="headband",

        rec_layer=5
    )
    store.mas_sprites.init_acs(orcaramelo_sakuya_izayoi_headband)




    mas_acs_promisering = MASSplitAccessory(
        "promisering",
        "promisering",
        MASPoseMap(
            p1=None,
            p2="2",
            p3="3",
            p4=None,
            p5="5",
            p6=None,
            p7=None,
        ),
        stay_on_start=True,
        acs_type="ring",
        rec_layer=MASMonika.ASE_ACS,
        arm_split=MASPoseMap(
            default="",
            p2="10",
            p3="10",
            p5="10"
        ),
        ex_props={
            "bare hands": True
        }
    )
    store.mas_sprites.init_acs(mas_acs_promisering)





    mas_acs_quetzalplushie = MASAccessory(
        "quetzalplushie",
        "quetzalplushie",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_q",
        mux_type=["plush_mid"] + store.mas_sprites.DEF_MUX_LD,
        entry_pp=store.mas_sprites._acs_quetzalplushie_entry,
        exit_pp=store.mas_sprites._acs_quetzalplushie_exit,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie)





    mas_acs_quetzalplushie_antlers = MASAccessory(
        "quetzalplushie_antlers",
        "quetzalplushie_antlers",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=12,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_antlers_entry,
        keep_on_desk=True
    )




    mas_acs_center_quetzalplushie = MASAccessory(
        "quetzalplushie_mid",
        "quetzalplushie_mid",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_mid",
        mux_type=["plush_q"],
        entry_pp=store.mas_sprites._acs_center_quetzalplushie_entry,
        exit_pp=store.mas_sprites._acs_center_quetzalplushie_exit,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_center_quetzalplushie)





    mas_acs_quetzalplushie_santahat = MASAccessory(
        "quetzalplushie_santahat",
        "quetzalplushie_santahat",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_santahat_entry,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie_santahat)

    mas_acs_quetzalplushie_center_santahat = MASAccessory(
        "quetzalplushie_santahat_mid",
        "quetzalplushie_santahat_mid",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_center_quetzalplushie_santahat_entry,
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie_center_santahat)

    velius94_bunnyscrunchie_blue = MASAccessory(
        "velius94_bunnyscrunchie_blue",
        "velius94_bunnyscrunchie_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="bunny-scrunchie",
        rec_layer=3,
        ex_props={
            "ribbon-like": True,
        },
    )
    store.mas_sprites.init_acs(velius94_bunnyscrunchie_blue)
    store.mas_selspr.init_selectable_acs(
        velius94_bunnyscrunchie_blue,
        "Синяя резинка для волос в форме заячьих ушек",
        "velius94_bunnyscrunchie_blue",
        "ribbon",
    )





    mas_acs_ribbon_black = MASAccessory(
        "ribbon_black",
        "ribbon_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_black,
        "Чёрная ленточка",
        "ribbon_black",
        "ribbon",
        hover_dlg=[
            "Это довольно формально, [player]."
        ],
        select_dlg=[
            "Мы идем в особенное место, [player]?"
        ]
    )




    mas_acs_ribbon_blank = MASAccessory(
        "ribbon_blank",
        "ribbon_blank",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blank)





    mas_acs_ribbon_blue = MASAccessory(
        "ribbon_blue",
        "ribbon_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_blue,
        "Синяя ленточка",
        "ribbon_blue",
        "ribbon",
        hover_dlg=[
            "Как океан..."
        ],
        select_dlg=[
            "Хороший выбор, [player]!"
        ]
    )





    mas_acs_ribbon_darkpurple = MASAccessory(
        "ribbon_dark_purple",
        "ribbon_dark_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_darkpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_darkpurple,
        "Тёмно-фиолетовая ленточка",
        "ribbon_dark_purple",
        "ribbon",
        hover_dlg=[
            "Мне нравится этот цвет!"
        ],
        select_dlg=[
            "Лаванда - хорошая смена темпа."
        ]
    )





    mas_acs_ribbon_emerald = MASAccessory(
        "ribbon_emerald",
        "ribbon_emerald",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_emerald)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_emerald,
        "Изумрудная ленточка",
        "ribbon_emerald",
        "ribbon",
        hover_dlg=[
            "Мне всегда нравился этот цвет...",
        ],
        select_dlg=[
            "Он такой же, как и мои глаза!"
        ]
    )




    mas_acs_ribbon_def = MASAccessory(
        "ribbon_def",
        "ribbon_def",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_def)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_def,
        "Белая ленточка",
        "ribbon_def",
        "ribbon",
        hover_dlg=[
            "Ты скучаешь по моей старой ленточке, [player]?"
        ],
        select_dlg=[
            "Возвращаемся к классике!"
        ]
    )





    mas_acs_ribbon_gray = MASAccessory(
        "ribbon_gray",
        "ribbon_gray",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gray)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gray,
        "Серая ленточка",
        "ribbon_gray",
        "ribbon",
        hover_dlg=[
            "Как в теплый, дождливый день..."
        ],
        select_dlg=[
            "Это действительно уникальный цвет, [player]."
        ]
    )





    mas_acs_ribbon_green = MASAccessory(
        "ribbon_green",
        "ribbon_green",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_green)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_green,
        "Зелёная ленточка",
        "ribbon_green",
        "ribbon",
        hover_dlg=[
            "Это прекрасный цвет!"
        ],
        select_dlg=[
            "Зелёная, как мои глаза!"
        ]
    )





    mas_acs_ribbon_lightpurple = MASAccessory(
        "ribbon_light_purple",
        "ribbon_light_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lightpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lightpurple,
        "Светло-фиолетовая ленточка",
        "ribbon_light_purple",
        "ribbon",
        hover_dlg=[
            "Этот фиолетовый выглядит довольно красиво, правда, [player]?"
        ],
        select_dlg=[
            "В ней и вправду чувствуется весна."
        ]
    )





    mas_acs_ribbon_peach = MASAccessory(
        "ribbon_peach",
        "ribbon_peach",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_peach)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_peach,
        "Персиковая ленточка",
        "ribbon_peach",
        "ribbon",
        hover_dlg=[
            "Какая красота!"
        ],
        select_dlg=[
            "Похоже на осенние листья..."
        ]
    )





    mas_acs_ribbon_pink = MASAccessory(
        "ribbon_pink",
        "ribbon_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=[
            "ribbon",
            "bow",
        ],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_pink,
        "Розовая ленточка",
        "ribbon_pink",
        "ribbon",
        hover_dlg=[
            "Выглядит мило, правда?"
        ],
        select_dlg=[
            "Хороший выбор!"
        ]
    )





    mas_acs_ribbon_platinum = MASAccessory(
        "ribbon_platinum",
        "ribbon_platinum",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_platinum)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_platinum,
        "Платиновая ленточка",
        "ribbon_platinum",
        "ribbon",
        hover_dlg=[
            "Это интересный цвет, [player].",
        ],
        select_dlg=[
            "Мне очень нравится этот цвет, если честно."
        ]
    )





    mas_acs_ribbon_red = MASAccessory(
        "ribbon_red",
        "ribbon_red",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_red)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_red,
        "Красная ленточка",
        "ribbon_red",
        "ribbon",
        hover_dlg=[
            "Красный - красивый цвет!"
        ],
        select_dlg=[
            "Похоже на розы~"
        ]
    )





    mas_acs_ribbon_ruby = MASAccessory(
        "ribbon_ruby",
        "ribbon_ruby",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_ruby)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_ruby,
        "Рубиновая ленточка",
        "ribbon_ruby",
        "ribbon",
        hover_dlg=[
            "Это красивый оттенок красного."
        ],
        select_dlg=[
            "Разве она не выглядит мило?"
        ]
    )





    mas_acs_ribbon_sapphire = MASAccessory(
        "ribbon_sapphire",
        "ribbon_sapphire",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_sapphire)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_sapphire,
        "Сапфировая ленточка",
        "ribbon_sapphire",
        "ribbon",
        hover_dlg=[
            "Прямо как ясное летнее небо..."
        ],
        select_dlg=[
            "Отличный выбор, [player]!"
        ]
    )





    mas_acs_ribbon_silver = MASAccessory(
        "ribbon_silver",
        "ribbon_silver",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_silver)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_silver,
        "Серебряная ленточка",
        "ribbon_silver",
        "ribbon",
        hover_dlg=[
            "Мне нравится, как она выглядит.",
            "Мне всегда нравился серебряный цвет."
        ],
        select_dlg=[
            "Отличный выбор, [player]."
        ]
    )





    mas_acs_ribbon_teal = MASAccessory(
        "ribbon_teal",
        "ribbon_teal",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_teal)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_teal,
        "Бирюзовая ленточка",
        "ribbon_teal",
        "ribbon",
        hover_dlg=[
            "Выглядит очень по-летнему, верно?"
        ],
        select_dlg=[
            "Прямо как летнее небо."
        ]
    )





    mas_acs_ribbon_wine = MASAccessory(
        "ribbon_wine",
        "ribbon_wine",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_wine)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_wine,
        "Винная ленточка",
        "ribbon_wine",
        "ribbon",
        hover_dlg=[
            "Это замечательный цвет!"
        ],
        select_dlg=[
            "Формально! Мы с тобой сходим в какое-то особенное место, [player]?"
        ]
    )





    mas_acs_ribbon_yellow = MASAccessory(
        "ribbon_yellow",
        "ribbon_yellow",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_yellow)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_yellow,
        "Жёлтая ленточка",
        "ribbon_yellow",
        "ribbon",
        hover_dlg=[
            "Этот цвет напоминает мне о хорошем летнем дне!"
        ],
        select_dlg=[
            "Хороший выбор, [player]!"
        ]
    )


    mas_acs_ribbon_coffee = MASAccessory(
        "lanvallime_ribbon_coffee",
        "lanvallime_ribbon_coffee",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_coffee)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_coffee,
        "Кофейная ленточка",
        "lanvallime_ribbon_coffee",
        "ribbon",
        hover_dlg=[
            "Есть что-то в этом цвете, что мне очень нравится..."
        ],
        select_dlg=[
            "Как и мой кофе~"
        ]
    )

    mas_acs_ribbon_gold = MASAccessory(
        "lanvallime_ribbon_gold",
        "lanvallime_ribbon_gold",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gold)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gold,
        "Золотая ленточка",
        "lanvallime_ribbon_gold",
        "ribbon",
        hover_dlg=[
            "Всё так блестит..."
        ],
        select_dlg=[
            "Лучше, когда я с тобой!"
        ]
    )

    mas_acs_ribbon_hot_pink = MASAccessory(
        "lanvallime_ribbon_hot_pink",
        "lanvallime_ribbon_hot_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_hot_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_hot_pink,
        "Ярко-розовая ленточка",
        "lanvallime_ribbon_hot_pink",
        "ribbon",
        hover_dlg=[
            "Мило!"
        ],
        select_dlg=[
            "Напоминает мне кое-кого..."
        ]
    )

    mas_acs_ribbon_lilac = MASAccessory(
        "lanvallime_ribbon_lilac",
        "lanvallime_ribbon_lilac",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lilac)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lilac,
        "Сиреневая ленточка",
        "lanvallime_ribbon_lilac",
        "ribbon",
        hover_dlg=[
            "Это выглядит так, как будто это будет приятно пахнуть..."
        ],
        select_dlg=[
            "Совсем как ты!"
        ]
    )

    mas_acs_ribbon_lime_green = MASAccessory(
        "lanvallime_ribbon_lime_green",
        "lanvallime_ribbon_lime_green",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lime_green)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lime_green,
        "Лаймовая ленточка",
        "lanvallime_ribbon_lime_green",
        "ribbon",
        hover_dlg=[
            "Напоминает мне птицу, которая мне очень нравится!"
        ],
        select_dlg=[
            "Отличный выбор, ты же знаешь, как я люблю зелёный!"
        ]
    )

    mas_acs_ribbon_navy_blue = MASAccessory(
        "lanvallime_ribbon_navy_blue",
        "lanvallime_ribbon_navy_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_navy_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_navy_blue,
        "Тёмно-синяя ленточка",
        "lanvallime_ribbon_navy_blue",
        "ribbon",
        hover_dlg=[
            "Ты поклонник воды, [player]?"
        ],
        select_dlg=[
            "Ты всегда держишь моё сердце на плаву~"
        ]
    )

    mas_acs_ribbon_orange = MASAccessory(
        "lanvallime_ribbon_orange",
        "lanvallime_ribbon_orange",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_orange)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_orange,
        "Оранжевая ленточка",
        "lanvallime_ribbon_orange",
        "ribbon",
        hover_dlg=[
            "Отличный осенний цвет!"
        ],
        select_dlg=[
            "Я могу представить, как мы прижимаемся друг к другу на сеновале~"
        ]
    )

    mas_acs_ribbon_royal_purple = MASAccessory(
        "lanvallime_ribbon_royal_purple",
        "lanvallime_ribbon_royal_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_royal_purple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_royal_purple,
        "Королевская фиолетовая ленточка",
        "lanvallime_ribbon_royal_purple",
        "ribbon",
        hover_dlg=[
            "Могу я одолжить твою ручку?"
        ],
        select_dlg=[
            "Хочешь почитать книгу вместе?"
        ]
    )

    mas_acs_ribbon_sky_blue = MASAccessory(
        "lanvallime_ribbon_sky_blue",
        "lanvallime_ribbon_sky_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_sky_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_sky_blue,
        "Небесно-голубая ленточка",
        "lanvallime_ribbon_sky_blue",
        "ribbon",
        hover_dlg=[
            "Ты когда-нибудь наблюдал[mas_gender_none] за облаками?",
            "Доводилось ли тебе смотреть на облака?"
        ],
        select_dlg=[
            "Ты всегда заставляешь меня чувствовать, что я витаю в облаках, [player]."
        ]
    )

    mas_acs_ribbon_bisexualpride = MASAccessory(
        "anonymioo_ribbon_bisexualpride",
        "anonymioo_ribbon_bisexualpride",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_bisexualpride)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_bisexualpride,
        "Ленточка бисексуала",
        "anonymioo_ribbon_bisexualpride",
        "ribbon"
    )


    mas_acs_ribbon_blackandwhite = MASAccessory(
        "anonymioo_ribbon_blackandwhite",
        "anonymioo_ribbon_blackandwhite",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blackandwhite)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_blackandwhite,
        "Чёрно-белая ленточка",
        "anonymioo_ribbon_blackandwhite",
        "ribbon",
        select_dlg=[
            "Инь и янь..."
        ]
    )

    mas_acs_ribbon_bronze = MASAccessory(
        "anonymioo_ribbon_bronze",
        "anonymioo_ribbon_bronze",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_bronze)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_bronze,
        "Бронзовая ленточка",
        "anonymioo_ribbon_bronze",
        "ribbon",
    )

    mas_acs_ribbon_brown = MASAccessory(
        "anonymioo_ribbon_brown",
        "anonymioo_ribbon_brown",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_brown)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_brown,
        "Коричневая ленточка",
        "anonymioo_ribbon_brown",
        "ribbon",
    )

    mas_acs_ribbon_gradient = MASAccessory(
        "anonymioo_ribbon_gradient",
        "anonymioo_ribbon_gradient",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gradient)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gradient,
        "Градиентная ленточка",
        "anonymioo_ribbon_gradient",
        "ribbon",
        select_dlg=[
            "Классика с изюминкой!"
        ]
    )

    mas_acs_ribbon_gradient_lowpoly = MASAccessory(
        "anonymioo_ribbon_gradient_lowpoly",
        "anonymioo_ribbon_gradient_lowpoly",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gradient_lowpoly)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gradient_lowpoly,
        "Слабо-градиентная ленточка",
        "anonymioo_ribbon_gradient_lowpoly",
        "ribbon",
        select_dlg=[
            "Довольно абстрактно..."
        ]
    )

    mas_acs_ribbon_gradient_rainbow = MASAccessory(
        "anonymioo_ribbon_gradient_rainbow",
        "anonymioo_ribbon_gradient_rainbow",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gradient_rainbow)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gradient_rainbow,
        "Радужная ленточка",
        "anonymioo_ribbon_gradient_rainbow",
        "ribbon",
        select_dlg=[
            "Такие живые цвета!"
        ]
    )

    mas_acs_ribbon_polkadots_whiteonred = MASAccessory(
        "anonymioo_ribbon_polkadots_whiteonred",
        "anonymioo_ribbon_polkadots_whiteonred",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_polkadots_whiteonred)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_polkadots_whiteonred,
        "Красная ленточка в белый горошек",
        "anonymioo_ribbon_polkadots_whiteonred",
        "ribbon",
        select_dlg=[
            "Милая, как пуговица!"
        ]
    )

    mas_acs_ribbon_starsky_black = MASAccessory(
        "anonymioo_ribbon_starsky_black",
        "anonymioo_ribbon_starsky_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_starsky_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_starsky_black,
        "Звёздная чёрно-небесная ленточка",
        "anonymioo_ribbon_starsky_black",
        "ribbon",
        select_dlg=[
            "Проблеск космоса..."
        ]
    )

    mas_acs_ribbon_starsky_red = MASAccessory(
        "anonymioo_ribbon_starsky_red",
        "anonymioo_ribbon_starsky_red",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_starsky_red)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_starsky_red,
        "Звёздная красно-небесная ленточка",
        "anonymioo_ribbon_starsky_red",
        "ribbon",
        select_dlg=[
            "Звёздная ночь..."
        ]
    )

    mas_acs_ribbon_striped_blueandwhite = MASAccessory(
        "anonymioo_ribbon_striped_blueandwhite",
        "anonymioo_ribbon_striped_blueandwhite",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_striped_blueandwhite)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_striped_blueandwhite,
        "Ленточка с синими и белыми полосками",
        "anonymioo_ribbon_striped_blueandwhite",
        "ribbon",
        select_dlg=[
            "Подходит для дня на пляже!"
        ]
    )

    mas_acs_ribbon_striped_pinkandwhite = MASAccessory(
        "anonymioo_ribbon_striped_pinkandwhite",
        "anonymioo_ribbon_striped_pinkandwhite",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_striped_pinkandwhite)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_striped_pinkandwhite,
        "Ленточка с розовыми и белыми полосками",
        "anonymioo_ribbon_striped_pinkandwhite",
        "ribbon",
        select_dlg=[
            "Тоска по летнему дню..."
        ]
    )

    mas_acs_bow_black = MASAccessory(
        "multimokia_bow_black",
        "multimokia_bow_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="bow",
        mux_type=["ribbon", "bow"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_bow_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_bow_black,
        "Чёрный бантик",
        "multimokia_bow_black",
        "bow",
        select_dlg=[
            "Отличный выбор, [player]!",
            "Очень официально!",
            "Мы идём в какое-то особенное место?"
        ]
    )





    mas_acs_roses = MASAccessory(
        "roses",
        "roses",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        acs_type="flowers",
        keep_on_desk=True
    )
    store.mas_sprites.init_acs(mas_acs_roses)









default persistent._mas_acs_enable_quetzalplushie = False



default persistent._mas_acs_enable_promisering = False
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc

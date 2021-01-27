init python in mas_sprites:


    def register_image(name, d):
        """
        Thanks for nothing, RenPy

        Registers the existence of an image with `name`, and that the image
        used displayable d.

        IN:
            name - tuple of strings (tag, attributes)
            d - displayables
        """
        if store.mas_globals.is_r7:
            renpy.display.image.register_image(name, d)
        
        else:
            img_tag = name[0]
            img_attr = name[1:]
            existing_attrs = renpy.display.image.image_attributes[img_tag]
            
            
            renpy.display.image.images[name] = d
            
            if img_attr not in existing_attrs:
                existing_attrs.append(img_attr)

    def needs_closed_eye_variant(exp):
        """
        Checks if an exp needs a closed eye variation

        IN:
            exp - spritecode to check

        OUT:
            boolean - True if the given spritecode needs a closed eye variant, False otherwise
        """
        return exp[1] not in "hd"

    def is_wink_sprite(exp):
        """
        Checks if an exp is a wink sprite

        IN:
            exp - spritecode to check

        OUT:
            boolean - True if this is a wink sprite, False otherwise
        """
        return exp[1] in "kn"

    def needs_tear_atl(exp):
        """
        Checks if this spritecode needs a streaming tears atl

        IN:
            exp - spritecode to check

        OUT:
            boolean - True if so, False otherwise
        """
        return "ts" in exp[3:-1]

    def replace_eyes(exp, replacement_eyes):
        """
        Returns the sprite string for the closed eye variant

        IN:
            exp - exp to replace eyes
            replacement_eyes - spritecode part representing the replacement eyes

        OUT:
            closed eye representation of the given spritecode
        """
        pose = exp[:1]
        rest = exp[2:]
        return pose + replacement_eyes + rest

    def generate_static_sprite(exp):
        """
        Creates the DynamicDisplayable object for the given exp

        IN:
            exp - exp to make a closed eye version of
        """
        register_image(
            ("monika", exp + "_static"),
            store.DynamicDisplayable(
                store.mas_drawmonika_rk,
                character=store.monika_chr,
                **store.mas_sprite_decoder.parse_exp_to_kwargs(exp)
            )
        )

    def add_static_sprite_alias(exp):
        """
        Registers an alias for static sprites

        IN:
            exp to make an alias for

        ASSUMES:
            non-static version exists
        """
        register_image(
            ("monika", exp),
            renpy.display.image.images[("monika", exp + "_static")]
        )

    def generate_normal_sprite(exp):
        """
        Generates sprites for standard open/closed eye variants

        DOES NOT HANDLE WINKS/TEARS

        IN:
            exp - spritecode to generate sprites for
        """
        
        just_static = False
        if exp.endswith("_static"):
            
            exp = exp.replace("_static", "")
            just_static = True
        
        
        closed_eyes_variant = replace_eyes(exp, 'd')
        
        
        needs_atl = not just_static and needs_closed_eye_variant(exp)
        
        if needs_atl and not renpy.has_image("monika " + closed_eyes_variant):
            generate_static_sprite(closed_eyes_variant)
            add_static_sprite_alias(closed_eyes_variant)
        
        
        generate_static_sprite(exp)
        
        
        if needs_atl:
            if needs_tear_atl(exp):
                register_image(
                    ("monika", exp),
                    store.streaming_tears_transform(
                        "monika " + exp + "_static",
                        "monika " + closed_eyes_variant + "_static"
                    )
                )
            
            else:
                register_image(
                    ("monika", exp),
                    store.blink_transform(
                        "monika " + exp + "_static",
                        "monika " + closed_eyes_variant + "_static"
                    )
                )
        
        
        elif not just_static:
            add_static_sprite_alias(exp)

    def generate_wink_sprite(exp):
        """
        Generates wink sprites and their prerequisites
        """
        open_eye_variant = replace_eyes(exp, 'e')
        
        if not renpy.has_image(open_eye_variant):
            
            generate_normal_sprite(open_eye_variant)
        
        
        generate_static_sprite(exp)
        
        
        register_image(
            ("monika", exp),
            store.wink_transform(
                "monika " + exp + "_static",
                "monika " + open_eye_variant
            )
        )

    def generate_images(exp):
        """
        Generates sprites, aliases, and their prerequisites and adds them to the renpy.display.image.images map

        IN:
            exp - spritecode to generate
        """
        exp = unicode(exp)
        
        if is_wink_sprite(exp):
            generate_wink_sprite(exp)
        else:
            generate_normal_sprite(exp)
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc

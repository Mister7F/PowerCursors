PowerCursors
==================

PowerCursors is a Sublime Text package that makes the add/remove/select of multiple cursors more convenient with keyboard.

You can easily add a cursor and move it around while keeping all other cursors static. You can also choose between these cursors and remove them. When you are done putting cursors in positions, you can activate them and start moving and editing with all of them.

This is a fork of https://github.com/MaokaiLin/PowerCursors

Demos:
------------------

### Multiple Cursors
![Demo 1 of PowerCursors](https://raw.github.com/MaokaiLin/PowerCursors/screencast/demo1.gif "PowerCursors Screencast 1")

### Multiple Selections
![Demo 2 of PowerCursors](https://raw.github.com/MaokaiLin/PowerCursors/screencast/demo2.gif "PowerCursors Screencast 2")


Install PowerCursors for [Sublime Text](http://www.sublimetext.com/)
-------------------

### Using [Package Control](https://sublime.wbond.net/):

1. Run `Package Control: Install Package` command.
2. Search for `PowerCursors` and install.
3. Restart Sublime Text.
4. Enjoy the extra power of multiple cursors!

### Or manually, using git (not recommended):

Clone repository into Packages directory (can be found using `Preferences: Browse Packages` command in Sublime Text)

    git clone git://github.com/kaste/PowerCursors.git


How to use
-------------------

**No key-bindings are installed.  You have to define your own!**

For that open `Preferences: Key Bindings`.  Look at and maybe copy-paste the bindings for [Windows/Linux](https://github.com/kaste/PowerCursors/blob/master/Default%20(Windows).sublime-keymap) or [Mac](https://github.com/kaste/PowerCursors/blob/master/Default%20(OSX).sublime-keymap).

There are 6 commands in **PowerCursors**:

* ### Add cursor

    It adds a cursor and enters a transition mode where you can move the active cursor around without affecting the position of the cursor you just added.

    The command is `power_cursor_add`.

* ### Remove current cursor

    It removes the currently active cursor and activates the cursor right before the current cursor (position-wise).

    The command is `power_cursor_remove`.

* ### Select previous/next cursor

    It makes the currently active cursor static and activates the cursor right before/after the current cursor (position-wise).

    It also works when you already have multiple cursors. It makes all cursors static and activates only the last/first cursor. Now you are free to move only one of the cursors, or remove some of them without affecting the rest.

    The command is `power_cursor_select`, with an argument "forward" being either `true` or `false`.

* ### Activate all cursors

    It activates all cursors. Now when you move or edit, all cursors will respond, just like how the native multiple-cursor works in Sublime Text.

    The command is `power_cursor_activate`.

* ### Exit

    It exits the cursor transition status. All cursors you added will be removed and the normal cursor mode is resumed.

    The command is `power_cursor_exit`.

### Note

All the commands above also work for selections. For example, after selecting one region, you can add a new cursor and select a different region while keeping the one you chose before intact. You can select multiple regions this way, then activate all and replace texts in them. Feel free to explore more usage of the commands. They are quite robust and adaptable.


License
-------------------

This software is released under the terms of the MIT license.

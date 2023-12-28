from collections import ChainMap
import sublime
import sublime_plugin


PREFERENCE_KEY = "power_cursors_style"
# DEFAULT_STYLE = {"scope": "region.redish", "icon": "dot", "flags": "outline"}
DEFAULT_STYLE = {"scope": "transition_cursor", "icon": "dot", "flags": "fill"}
STYLES = {
    "fill": sublime.DRAW_EMPTY | sublime.PERSISTENT,
    "outline": sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL | sublime.PERSISTENT,
    "hidden": sublime.HIDDEN | sublime.PERSISTENT,
}
REGION_KEY = "transition_sels"


#### Helper functions for adding and restoring selections ####


def set_transition_sels(view, sels):
    """Set the updated transition selections and marks."""
    if sels:
        styles = ChainMap(
            view.settings().get(PREFERENCE_KEY) or {},
            DEFAULT_STYLE,
        )
        if isinstance(styles["flags"], str):
            try:
                styles["flags"] = STYLES[styles["flags"]]
            except LookupError:
                styles["flags"] = STYLES["hidden"]
        view.add_regions(REGION_KEY, sels, **styles)
        view.set_status("x_power_cursors", "{} saved selections".format(len(sels)))
    else:
        view.erase_regions(REGION_KEY)
        view.erase_status("x_power_cursors")


def find_prev_sel(trans_sels, current_sel):
    """Find the region in `trans_sels` that is right before `current_sel`.
    Assume `trans_sels` is sorted.
    """
    for i in range(len(trans_sels) - 1, -1, -1):
        if trans_sels[i].end() < current_sel.end():
            return i, trans_sels[i]

    # Rotate to the last if `current_sel` is before all other selections
    return -1, trans_sels[-1]


def find_next_sel(trans_sels, current_sel):
    """Find the region in `trans_sels` that is right after `current_sel`.
    Assume  `trans_sels` is sorted.
    """
    # for i, sel in enumerate(trans_sels):
    for i, sel in enumerate(trans_sels):
        if sel.begin() > current_sel.begin():
            return i, trans_sels[i]

    # Rotate to the beginning if `current_sel` is after all other selections
    return 0, trans_sels[0]


#### Commands ####


class power_cursor_add(sublime_plugin.TextCommand):
    """Add a new transition cursor in the view."""

    def run(self, edit, keep_alive_cursor_index=-1, keep_alive_cursor_position="b"):
        view = self.view

        # Store the current selection
        current_sels = [s for s in view.sel()]
        trans_sels = view.get_regions(REGION_KEY)
        trans_sels.extend(current_sels)
        set_transition_sels(view, trans_sels)

        # Keep one current cursor alive, depending on the given args
        view.erase_regions("mark")
        view.sel().clear()
        try:
            alive_sel = current_sels[keep_alive_cursor_index]
            alive_pos = {
                "a": alive_sel.a,
                "b": alive_sel.b,
                "begin": alive_sel.begin(),
                "end": alive_sel.end(),
            }[keep_alive_cursor_position]
        except Exception:
            # Fail safe
            alive_sel = current_sels[-1]
            alive_pos = alive_sel.b

        view.sel().add(sublime.Region(alive_pos, alive_pos))


class power_cursor_remove(sublime_plugin.TextCommand):
    """Remove the current transition cursor and switch back to the previous one."""

    def run(self, edit) -> None:
        view = self.view

        # Retrieve the transition selections
        trans_sels = view.get_regions(REGION_KEY)
        if len(trans_sels) == 0:
            return

        def row_of(x) -> int:
            return view.rowcol(x)[0]

        # Activate the selection that is closest to the current selection(s)
        # in terms of lines
        cursor = view.sel()[-1].b
        row_of_cursor = row_of(cursor)
        _, _, new_sel, index = min(
            (
                min(
                    abs(row_of(sel.b) - row_of_cursor),
                    abs(row_of(sel.a) - row_of_cursor),
                ),
                min(abs(sel.b - cursor), abs(sel.a - cursor)),
                sel,
                i,
            )
            for i, sel in enumerate(trans_sels)
        )

        view.sel().clear()
        view.sel().add(new_sel)
        view.show(new_sel)
        if new_sel.a != new_sel.b:
            view.add_regions(
                "mark",
                [sublime.Region(new_sel.a, new_sel.a)],
                "mark",
                "dot",
                sublime.HIDDEN | sublime.PERSISTENT,
            )
        else:
            view.erase_regions("mark")

        del trans_sels[index]
        set_transition_sels(view, trans_sels)


class power_cursor_select(sublime_plugin.TextCommand):
    """Switch back and forth between transition cursors."""

    def run(self, edit, forward=False):
        view = self.view

        current_sels = [s for s in view.sel()]
        trans_sels = view.get_regions(REGION_KEY)
        # Add the current selections into the transition lists but not if you
        # have a single cursor right now *and* only selections in the list.
        if (
            all(not s.empty() for s in trans_sels)
            and len(current_sels) == 1
            and current_sels[0].empty()
        ): ...
        else:
            trans_sels.extend(current_sels)
            # Lazy step: Store the disorganized region and retrieve a sorted and
            # merged region list
            view.add_regions(REGION_KEY, trans_sels)
            trans_sels = view.get_regions(REGION_KEY)

        # Get the previous or next selection and mark
        if forward:
            index, sel = find_next_sel(trans_sels, current_sels[0])
        else:
            index, sel = find_prev_sel(trans_sels, current_sels[-1])

        # Activate the selection
        view.sel().clear()
        view.sel().add(sel)
        view.show(sel)
        if sel.a != sel.b:
            view.add_regions(
                "mark",
                [sublime.Region(sel.a, sel.a)],
                "mark",
                "dot",
                sublime.HIDDEN | sublime.PERSISTENT,
            )

        # Remove it from transition list
        del trans_sels[index]
        set_transition_sels(view, trans_sels)


class power_cursor_activate(sublime_plugin.TextCommand):
    """Activate all cursors (including the one that's currently alive)."""

    def run(self, edit):
        view = self.view
        trans_sels = view.get_regions(REGION_KEY)
        current_sels = [s for s in view.sel()]
        # Add the current selections into the transition lists but not if you
        # have a single cursor right now *and* only selections in the list.
        if (
            all(not s.empty() for s in trans_sels)
            and len(current_sels) == 1
            and current_sels[0].empty()
        ):
            view.sel().clear()
        view.sel().add_all(trans_sels)
        set_transition_sels(view, [])
        view.erase_regions("mark")


class power_cursor_exit(sublime_plugin.TextCommand):
    """Clear all transition cursors and exit the transition state."""

    def run(self, edit):
        set_transition_sels(self.view, [])


class CursorTransitionListener(sublime_plugin.EventListener):
    """Provide the transition status for context queries."""

    def on_query_context(self, view, key, operator, operand, match_all):
        if key == "in_cursor_transition":
            in_transition = len(view.get_regions(REGION_KEY)) > 0
            return (
                in_transition == operand
                if operator == sublime.OP_EQUAL
                else in_transition
            )

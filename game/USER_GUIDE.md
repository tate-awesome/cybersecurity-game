# Getting Around the Cyber-ICS Training Module

This guide covers how to use the app itself: getting between pages, the buttons
every page has, laying out panels, the settings, and what the app saves for you.
It doesn't cover lesson content or what each panel does. The lessons explain those.

- **Part 1, the basics.** Read this on your first day.
- **Part 2, power user.** Read this once the basics feel easy.
- **Cheat sheet.** One page to keep open.

---

# Part 1: The Basics

## 1. The three kinds of page

The app has three kinds of page:

1. **The title page.** You land here when the app starts. It has three big
   buttons:
   - **Start** opens the workspace list. When a workspace is bookmarked, a
     **Resume in *workspace*** button sits beside it. See
     [Bookmarks and Resume](#5-bookmarks-and-resume).
   - **Settings** opens the settings page.
   - **Quit** closes the app.

   Along the bottom of the title page are links to the project's **Source Code**
   and to **Report an Issue**. Both open in your web browser.

2. **The workspace list** (titled *Workspaces*). The sidebar on the left lists
   every workspace, grouped into collapsible sections. Click a section header to
   open or close it.
   - **Click** a workspace to read its summary on the right.
   - **Double-click** it, or press **Open Workspace** on the summary, to go in.

   The list remembers the last workspace you selected and has it selected the
   next time you come back.

3. **Workspaces.** This is where the lessons happen. A workspace is a set of
   **panels** laid out side by side and stacked, under a **menu bar** at the top
   and above a **footer** at the bottom. Most of this guide is about workspaces.

The settings page and a few others are ordinary pages with a menu bar, just
without panels.

## 2. The parts of the screen

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ☰  «  »  Page Title  🔖 ⟳   [page tools ...]          ⚙  ?  │  –   ▢   ⏻    │  ← menu bar
├──────────────────────────────────────────────────────────────────────────────┤
│ ┌─ – Panel A ─────────────┐ ┌─ – Panel B ──────────────────────────────────┐ │
│ │                         │ │                                              │ │
│ │                         │ │                                              │ │
│ └─────────────────────────┘ └──────────────────────────────────────────────┘ │
│ ┌─ – Panel C │ Panel D │ ··· ───────────────────────────────────────────────┐ │  ← a tabbed pane
│ │                                                                          │ │
│ └──────────────────────────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────────┤
│ where you are · Wi-Fi · theme · background │ fps · zoom · session · version  │  ← footer
└──────────────────────────────────────────────────────────────────────────────┘
```

The app has no regular window frame. The **menu bar is the title bar**:

- Drag any empty part of it, or the page title, to move the window.
- **Double-click** it to maximize the window, or to restore it if it's already
  maximized.
- Drag the window's edges or corners to resize it. This doesn't work while the
  window is maximized or fullscreen.

## 3. Buttons on every page

Every page with a menu bar has the same buttons on its left and right ends.
**Hover over any button to see what it does.** Every button has a tooltip, and
the Back and Forward tooltips name the page they go to.

### Left end, from left to right

| Icon | Button | What it does |
| --- | --- | --- |
| ☰ | **Menu** | Opens the [menu drawer](#4-the-menu-drawer-esc). **Esc** does the same. |
| « | **Back** | Goes to the previous page. Greyed out when there's no previous page. |
| » | **Forward** | Goes forward again to the page you just went back from. Greyed out when there's nowhere to go. |
| *Title* | Page title | Just a name, but you can drag it to move the window. |
| 🔖 | **Bookmark** | Bookmarks this workspace for the title page's Resume button. Click it again to remove the bookmark. The icon is filled while this page is the bookmarked one. |
| ⟳ | **Refresh** | Rebuilds the page and asks you to confirm first. On a workspace it also puts the panels back in their default places and sizes, but **keeps your inputs and anything running**. |

### Middle: page tools

Between the two ends are the page's own buttons, for example **Manage Captures**,
**ModBus Settings**, **View**, **Edit Workspace** and **Links** on many
workspaces. These differ from workspace to workspace. A button with a caret opens
a dropdown with headed sections.

When the window is too narrow, page tools that don't fit move into a **»»
(More buttons)** button. Click it to reach them.

### Right end, from left to right

| Icon | Button | What it does |
| --- | --- | --- |
| ⚙ (sliders) | **Quick Settings** | A dropdown with the settings people change most. See [Quick Settings](#9-quick-settings). |
| ? | **Help** | Shows a help message for the current page. |
| – | **Minimize** | Minimizes the window to your taskbar or dock. |
| ▢ / ⧉ | **Maximize / Restore Down** | Maximizes the window, or restores it. Hidden while fullscreen. |
| ⏻ | **Quit** | Closes the app. It **asks first**, because anything still running will be stopped. |

The title pages have no menu bar, but Quick Settings, Help and the three window
buttons still sit in the top-right corner.

## 4. The menu drawer (Esc)

Press **Esc** or click **☰** and a menu slides out from the left edge. It lists
**every button on the menu bar with its name written out**, so you never have to
guess what an icon means. From top to bottom:

1. **Resume** (closes the menu), **Back to *page***, **Forward to *page***,
   **Bookmark this Workspace** / **Remove Bookmark**, and **Refresh**.
2. This page's tools, in a card under the page's title.
3. Quick Settings, Settings and Help.
4. Minimize, Maximize/Restore and **Quit**.
5. **What's running right now**, for example "*NMap running*", or *Nothing
   running*. Check this before you leave a page.

The menu doesn't pause anything. The page keeps running, just dimmed. Close the
menu with **Esc** again, or by clicking anywhere outside it.

## 5. Bookmarks and Resume

- In a workspace, click **🔖 Bookmark**. You can only bookmark one workspace at a
  time.
- Next time you start the app, the title page shows **Resume in *workspace***
  next to Start. Click it to jump straight back in.
- You can also choose the bookmarked workspace under **Settings → General →
  Navigation → Favorite Workspace**, or set it to *None* there.

## 6. Leaving a page stops what's running

When you **leave a workspace** (Back, Forward, a link, Workspaces, or quitting),
the app **stops everything that workspace was running** and starts the next page
fresh. **Refresh** and **zoom** rebuild the page without stopping anything.

> Want to look at something on another page without stopping your work? Open the
> menu (**Esc**) and check the "running" line before you go.

## 7. Working with panels

Every panel has its own small menu bar: a **– minimize button**, its **title**
(or its tabs), and sometimes buttons of its own. If a panel's buttons don't fit,
they move into a **»» (More buttons)** button, just like on the page's menu bar.

### Resize

Drag the **gap between two panels** to share the space differently.

### Minimize and restore

- Click **–** at the far left of a panel's bar. The panel shrinks to just its bar
  and its neighbours take the space.
- Click the **square** (**Maximize**) in the same spot to bring it back at the
  size it had before.
- **Shortcut:** dragging a gap until a panel is as thin as its bar minimizes it.
  Dragging it back open restores it, at whatever size you drag it to.
- When **every** panel in a row or column is minimized, the whole group lies flat
  the other way. It becomes a thin strip of **sideways titles** with a restore
  button at the top. Click the restore button, or any one title, to open the
  group back up.
- The outermost group can't be minimized, because nothing would be left to take
  its space.

### Peek: look at a minimized panel without restoring it

A minimized panel has a small **caret (˅) next to its title**. On a sideways
strip, **clicking a title** does the same thing. Click it to **peek**: the panel
opens in a popup over the layout, at full size and fully usable, while
everything else stays where it is.

To put it away, click outside the popup, click the caret again, or press
**Esc**.

### Move a panel (docking)

1. **Press and hold** on an empty part of the panel's bar, its title or one of
   its tabs. Don't press its buttons.
2. **Drag.** The panel stays where it is, faded, and a chip with its name follows
   your mouse.
3. As you move, a **see-through rectangle shows where it will land**:

   | Where you let go over another panel | Result |
   | --- | --- |
   | **Middle** of the panel | Added to that panel as a **tab** |
   | Near its **left, right, top or bottom edge** | Placed **beside** it, splitting that space in two |
   | Inside a panel's **row of tabs** | Inserted as a tab **at that spot** in the row |
   | In the **thin band right at the edge** of a whole row or column | Placed beside **the whole group**, not just one panel |

4. **Release** to drop it. Nothing in the layout moves until you drop.
5. Changed your mind? Press **Esc** while dragging, or drop it back where it
   started.

You can build any layout with these drops.

### Tabs

When two or more panels share one space, the bar shows a **tab for each one**,
with the current tab highlighted.

- **Click a tab** to switch to it.
- **Drag a tab** to pull that panel out somewhere else, or to reorder it.
- If there isn't room for every tab, a **···** button lists the rest.

### Undo your layout changes

There are two ways to put the panels back in their default places and sizes,
while **keeping your inputs**:

- **Refresh** (⟳) on the menu bar.
- **Edit Workspace → Reload → Reset Layout** (on workspaces that have it).

## 8. The footer

The bar along the bottom is on every page. Hover over any part of it for more
detail.

| Part | Shows | Hover for |
| --- | --- | --- |
| Location | The page you're on | Your page history: Back goes up one |
| Wi-Fi | The network you're on, and whether it's *home* or the *device* | The home network, the device name, and your saved networks |
| Theme | Light or dark, and the theme name | The other appearance settings |
| Background | The animated background and its frame rate | What it's showing, and whether it's still or detailed |
| DEV / Label Keys | Shown only when developer mode or debug labels are on | What that means |
| fps | Frames drawn per second: what's achieved / what's targeted | (F3 shows more) |
| Zoom | The current zoom %, and "Fullscreen" when you're fullscreen | **Every keyboard shortcut** |
| Session | How long the app has been open | When it started |
| Version | The app's version | Commit, branch and build details |

## 9. Quick Settings

**⚙ Quick Settings** (top right of every page) holds the settings you'll change
most often:

- **General:** **Enter/Exit Fullscreen**, and **Localization** (load the app's
  text in another language from a file).
- **Appearance:** **Enable Light/Dark Mode**, **Select Theme**, and **Select
  Background** (the animated picture behind pages, or none).
- **Navigation:** **Open AP-Config Page** (in your browser) and **Settings**
  (the full settings page).

Everything else is on the settings page.

## 10. The settings page

Open it from **Quick Settings → Settings**, or from **Settings** on the title
page. Changes apply **immediately** and are **saved automatically**, so there's
no Save button. The page reopens on the tab you were last on.

### General

| Section | Settings |
| --- | --- |
| **Display** | **Fullscreen** |
| **Language** | **Labels File** (which one is in use), **Load Labels**, **Use Default** |
| **Navigation** | **Favorite Workspace**, the one Resume opens |

### Appearance

| Section | Settings |
| --- | --- |
| **Theme** | **Light or Dark Mode**, **Theme**, **Import Themes** (opens a folder: drop theme `.json` files in and they show up in the list), **Invert Buttons** (plain outlined buttons instead of colored ones) |
| **Animated Background** | **Background Type**, plus **All Animations** to try every background on a preview page |
| **Window Effects** | **Fade In** on startup, **Fade Out** on quit |
| **Reset** | **Appearance**: back to the default theme in your system's mode, and the default background and effects |

### Graphics

| Section | Settings |
| --- | --- |
| **Quality Preset** | **Low** (slow computers), **Balanced** (default), **High** (smoothest). Changing any setting below switches this to *Custom*. |
| **Frame Rate** | **Panel Framerate** (1–60), **Background Framerate** (1–120) |
| **Rendering** | **Antialiasing**, **Transitions** (animated page changes and popups), **Smooth Scrolling**, **Freeze Background**, **Freeze Background in Workspaces**, **Disable Background in Workspaces**, **Detailed Background** |
| **Reset** | **Graphics**: every setting on this tab |

### Keybinds

Click a box and **press the keys** you want. Clear the box to unbind. If those
keys already belong to another action, they move to this one.

| Action | Default |
| --- | --- |
| Zoom In | **Ctrl +** (Ctrl = also works) |
| Zoom Out | **Ctrl −** |
| Reset Zoom | *unbound*. Set it yourself. |
| Toggle Fullscreen | **F11** |
| Toggle Developer Mode | **F12** |

**Keybinds** resets them all. **F3** (performance overlay) and **Esc** (menu)
can't be changed.

### Troubleshooting

| Section | Settings |
| --- | --- |
| **Reset Settings** | Reset **Appearance**, **Graphics**, **Keybinds** or **Default Labels** on their own. Nothing else changes. |
| **Saved Data** | **Workspace Data**: every workspace's saved inputs and layouts go back to default. Your settings are kept. **Asks first, and can't be undone.** |
| **Monitoring** | **Performance Overlay**: frame rates, slow panels and load times in a corner. Same as **F3**. |

### Advanced

| Section | Settings |
| --- | --- |
| **Privileged Network Helper** | **Use Helper Process**: runs packet capture in a separate administrator process, which keeps the main app responsive under heavy traffic. Asks for administrator access when you turn it on. |
| **Theme Editor** | Build your own theme. If you make something unreadable, **Appearance → Reset** undoes it. |
| **Access Point** | **Configuration Page**: opens the access point's page in your browser |
| **Diagnostics** | **Log Timings**: prints performance measurements to the console the app was started from |
| **Full Reset** | **All User Data**: wipes *everything* (workspace data, captures, every setting). **Asks first, and can't be undone.** |
| **Developer Mode** | For instructors and developers. See [Developer mode](#developer-mode). |

### Developer (only while developer mode is on)

**Debug Labels** and **Edit Workspaces**.

---

## 11. What's saved for you

You never need to press Save to keep your place. The app saves to the
`user_data/` folder next to the app.

### Saved automatically

| What | When | Kept for |
| --- | --- | --- |
| **Every setting** on the settings page and in Quick Settings: theme, light/dark, background, graphics, keybinds, language file, fullscreen, fade in/out, developer mode | The moment you change it | All workspaces, across restarts |
| **Your bookmark** (Favorite Workspace) | When you click Bookmark or change it in Settings | Across restarts |
| **The last workspace selected** on the workspace list | When you select it | Across restarts |
| **Each workspace's inputs:** form entries, toggles, register settings, display styles, the cards and forms you've shown/hidden and their order, packet console columns, which hosts are hidden | When you **leave the workspace**, **refresh** it, **zoom**, or **quit** | That workspace only |
| **Each workspace's layout:** where you docked panels, tab groups, and the sizes you dragged them to | Same as above | That workspace only |
| **Device nicknames** (Configure Hosts) | As you type them | Every workspace |
| **Wi-Fi home network and device name** | As you enter them | Every workspace |
| **A rolling session log** of recent packets, status messages and actions | Continuously in the background | About the **last 15 minutes**, up to 256 MB. Older parts are deleted automatically. |

Only what you **changed** is saved. A workspace you never touched has no saved
data, so if the lesson's defaults are updated later, you get the new ones.

### Not saved

- **Zoom.** Every launch starts at 100%.
- **Which panels are minimized.** Panels open back up the next time you enter
  the workspace.
- **Paused consoles.** A workspace always opens with its packet console live.
- **Anything running** (scans, attacks, captures in progress). It stops when you
  leave the workspace or quit.
- **Captured data**, unless you save it yourself with **Manage Captures → Save
  Current Capture** or **Start Streaming to JSON Capture File**.

### Clearing saved data

From the gentlest to the most drastic:

| Where | What it clears |
| --- | --- |
| **Refresh** ⟳, or **Edit Workspace → Reset Layout** | This workspace's **layout** only |
| **Edit Workspace → Reset Inputs** | This workspace's **inputs** only. The layout is kept. |
| **Edit Workspace → Reset Workspace** | This workspace's inputs **and** layout |
| **Settings → Troubleshooting → Reset Settings** | One group of settings |
| **Settings → Troubleshooting → Workspace Data** | **Every** workspace's inputs and layout. Settings are kept. |
| **Settings → Advanced → All User Data** | **Everything** |

Each of these asks you to confirm first.

---

# Part 2: Power User

## Keyboard shortcuts

| Keys | Action | Can be changed? |
| --- | --- | --- |
| **Esc** | Open or close the menu drawer. Also closes any dropdown or peek, and cancels a panel drag. | No |
| **F11** | Toggle fullscreen (and remember it for next launch) | Yes |
| **Ctrl +** / **Ctrl =** | Zoom in | Yes |
| **Ctrl −** | Zoom out | Yes |
| *(bind it yourself)* | Reset zoom to 100% | Yes |
| **F3** | Performance overlay | No |
| **F12** | Toggle developer mode | Yes |
| **Ctrl F** | Find on the page, on pages with a search bar (the workspace editor). **Enter** / **Shift Enter** steps through matches. | No |
| **Shift + mouse wheel** | Scroll **sideways** everywhere: scroll areas, horizontal sliders, and chart zoom where a chart supports it | No |

Forgot one? Hover over **Zoom** in the footer to see the list with your current
bindings.

## Zoom

Zoom steps through 25, 33, 50, 67, 75, 80, 90, **100**, 110, 125, 133, 140, 150,
175, 200, 250, 300, 400 and 500%. Each step rebuilds the page. Your workspace
is saved first and nothing running is stopped, so zooming is safe at any time.
Zoom resets to 100% when you restart, so bind **Reset Zoom** if you change zoom
often.

## Layout tricks

- **Peek instead of restoring.** Keep reference panels minimized and peek (˅) at
  them when you need them. The layout never shifts.
- **Collapse a whole side with one drag.** Drag the gap until the group is as
  thin as a bar and the whole group minimizes into a sideways strip. Click any
  sideways title to open the group with that panel showing.
- **Restore to an exact size.** Instead of clicking the square, drag a minimized
  panel's gap open. It restores at the size you drag to.
- **Stack panels you switch between** as tabs (drop in the middle), and **put
  panels you compare side by side** (drop near an edge).
- **Span a whole row or column.** Drop into the thin band at the very edge of a
  group to dock beside the *whole* group, not just one panel. This is how you
  make a panel run the full width or height.
- **Experiment freely.** Refresh (⟳) always gets you back to the default layout
  without losing your inputs.
- **Narrow window?** Buttons that don't fit go into **»»** on both the page and
  panel bars. Nothing disappears for good.

## Window tricks

- **Double-click the menu bar** to maximize or restore the window.
- On Windows, dragging the menu bar to the top of the screen maximizes the
  window, and dragging it to a side snaps it, like any other window.
- Dragging the bar of a maximized window restores it under your cursor.
- **Fullscreen** (F11) hides Maximize, but Minimize and Quit stay.

## Dropdown tricks

- Dropdowns (Quick Settings, page tool groups, overflow) close with **Esc** or a
  click outside them.
- **Right-click inside an open dropdown** and choose **Screenshot to Clipboard**.
  While a dropdown is open it holds the keyboard, so this is the way to capture
  it.

## Navigation tricks

- **Hover over Back/Forward** to see where they go before you click.
- **Hover over the footer's location** to see your whole page history.
- **Bookmark** the workspace you're working through, and you can jump straight
  back in with **Resume** next time you start the app.
- On the workspace list, **double-click** a workspace to skip the summary.
- Before leaving a workspace, glance at **Esc → "… running"** so you don't stop
  something by accident.

## Performance tuning

If the app feels slow:

1. Press **F3** to see which panels are slow and what frame rate you're
   actually getting. The footer's **fps** shows achieved / target all the time.
2. **Settings → Graphics → Quality Preset → Low**, or tune it yourself:
   - lower **Panel Framerate**
   - turn on **Freeze Background in Workspaces** or **Disable Background in
     Workspaces**
   - turn off **Antialiasing**, **Transitions** and **Smooth Scrolling**
3. Under heavy network traffic, try **Settings → Advanced → Use Helper Process**.
4. If something looks wrong, **Settings → Troubleshooting** resets one group of
   settings at a time.

## Make it yours

- **Themes:** pick one in Quick Settings. For full control, use **Settings →
  Advanced → Theme Editor** to make a **New Theme** from any existing one, tune
  every color, and **Save**. To share themes, drop `.json` theme files into the
  folder that **Import Themes** opens.
- **Backgrounds:** **Settings → Appearance → All Animations** previews every
  background. **Cycle All** rotates through them every 20 seconds.
- **Language / wording:** **Load Labels** replaces the app's text with a labels
  file. Anything the file doesn't cover keeps its default text.

## Developer mode

Press **F12**, or turn it on under **Settings → Advanced**. A **DEV** tag shows
in the footer while it's on. It's meant for instructors and developers, and it
adds:

- A **Debug Tools** section in Quick Settings: **Edit Workspaces**, **Edit This
  Workspace**, **Material Editor**, **Save Layout Shape/Weights as Default**,
  **Save Current Columns as Default**, **Edit Availability**, **Debug Labels**,
  and delete-data shortcuts.
- A **Developer** tab on the settings page.
- An **Edit This Workspace** button on the workspace list's summary.

These tools change the workspaces themselves for **everyone**, not just your own
saved data. Press **F12** again to switch it off.

---

# Cheat sheet

```
GETTING AROUND                       PANELS
  Esc .......... menu (everything)     – ............ minimize        ▢ ...... restore
  « » .......... back / forward        ˅ ............ peek at a minimized panel
  🔖 ............ bookmark → Resume    drag bar ..... move: middle = tab, edge = beside
  ⟳ ............ refresh / reset layout  drag gap ..... resize (thin enough = minimize)
  Leaving a workspace STOPS what's running   ··· ...... hidden tabs   »» .. hidden buttons

WINDOW                               KEYS
  drag bar ..... move window           F11 .......... fullscreen    F3 .... performance
  dbl-click bar  maximize/restore      Ctrl + / − ... zoom          F12 ... developer mode
  ⏻ ............ quit (asks first)     Shift+wheel .. scroll sideways

AUTOSAVED: settings instantly; each workspace's inputs + layout when you leave,
refresh, zoom or quit. NOT SAVED: zoom, minimized panels, running actions,
captures (unless you save them).
```

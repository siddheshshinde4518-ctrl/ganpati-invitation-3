from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp


class ClickableDoor(ButtonBehavior, Image):
    """The entire door image acts as the button."""
    pass


class Invitation(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.opened = False
        self.invitation_event = None

        # ==========================================
        # DOOR
        # ==========================================

        self.door = ClickableDoor(
            source="door.png",
            allow_stretch=True,
            keep_ratio=False,
            opacity=1
        )

        self.add_widget(self.door)

        # ==========================================
        # GANPATI BAPA
        # ==========================================

        self.ganesha = Image(
            source="ganesha.png",
            size_hint=(None, None),
            allow_stretch=True,
            keep_ratio=True,
            opacity=0
        )

        self.add_widget(self.ganesha)

        # ==========================================
        # INVITATION TEXT
        # ==========================================

        self.card = Label(
            text=(
                "✨  INVITATION  ✨\n\n"
                "With great joy,\n"
                "we invite you to our celebration\n\n"
                "🙏 Please join us 🙏"
            ),
            halign="center",
            valign="middle",
            color=(1, 0.85, 0.20, 1),
            bold=True,
            opacity=0
        )

        self.add_widget(self.card)

        # Door is clickable
        self.door.bind(on_release=self.open_invitation)

        # Responsive layout
        self.bind(
            size=self.update_layout,
            pos=self.update_layout
        )

        Clock.schedule_once(self.update_layout, 0)

    # ==========================================
    # RESPONSIVE LAYOUT
    # ==========================================

    def update_layout(self, *args):

        w = self.width
        h = self.height

        if w <= 0 or h <= 0:
            return

        smallest = min(w, h)

        # Door fills the entire screen
        self.door.pos = self.pos
        self.door.size = self.size

        # Ganpati Bapa
        ganesha_size = smallest * 0.90

        self.ganesha.size = (
            ganesha_size,
            ganesha_size
        )

        self.ganesha.center = (
            self.center_x,
            self.center_y
        )

        # Invitation
        self.card.pos = (
            w * 0.08,
            h * 0.10
        )

        self.card.size = (
            w * 0.84,
            h * 0.80
        )

        self.card.text_size = self.card.size

        # Responsive text size
        self.card.font_size = max(
            dp(18),
            smallest * 0.045
        )

    # ==========================================
    # OPEN DOOR
    # ==========================================

    def open_invitation(self, *args):

        if self.opened:
            return

        self.opened = True

        # Cancel previous event if necessary
        if self.invitation_event:
            self.invitation_event.cancel()
            self.invitation_event = None

        # Stop previous animations
        Animation.cancel_all(self.door)
        Animation.cancel_all(self.ganesha)
        Animation.cancel_all(self.card)

        # Door fades away
        Animation(
            opacity=0,
            duration=1.5,
            t="out_cubic"
        ).start(self.door)

        # Ganpati Bapa appears
        Animation(
            opacity=1,
            duration=1.2,
            t="out_back"
        ).start(self.ganesha)

        # Wait before showing invitation
        self.invitation_event = Clock.schedule_once(
            self.show_invitation,
            3
        )

    # ==========================================
    # SHOW INVITATION
    # ==========================================

    def show_invitation(self, dt):

        self.invitation_event = None

        # Ganpati fades away
        Animation(
            opacity=0,
            duration=0.7,
            t="in_out_quad"
        ).start(self.ganesha)

        # Then show invitation
        Clock.schedule_once(
            self.animate_card,
            0.6
        )

    # ==========================================
    # INVITATION ANIMATION
    # ==========================================

    def animate_card(self, dt):

        original_y = self.card.y

        # Start slightly lower
        self.card.y = original_y - dp(30)

        # Fade + slide upward
        Animation(
            opacity=1,
            y=original_y,
            duration=1.2,
            t="out_back"
        ).start(self.card)

    # ==========================================
    # RESET
    # ==========================================

    def reset_invitation(self):

        self.opened = False

        if self.invitation_event:
            self.invitation_event.cancel()
            self.invitation_event = None

        Animation.cancel_all(self.door)
        Animation.cancel_all(self.ganesha)
        Animation.cancel_all(self.card)

        self.door.opacity = 1
        self.ganesha.opacity = 0
        self.card.opacity = 0

        self.update_layout()


class MyApp(App):

    title = "Ganpati Invitation"

    def build(self):
        return Invitation()


if __name__ == "__main__":
    MyApp().run()
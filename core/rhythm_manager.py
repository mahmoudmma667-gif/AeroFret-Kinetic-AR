"""
AeroFret: Kinetic - Rhythm Game Manager (Guitar Hero Mode)
Manages falling musical targets, timing & spatial accuracy measurement (Perfect, Good, Miss),
dynamic combo multipliers, floating hit judgments, and game scoring statistics.
"""

import math
import random
import time
from typing import Dict, List, Optional, Tuple


class RhythmNote:
    """Represents a falling musical note target."""

    def __init__(
        self,
        note_id: int,
        string_index: int,
        target_chord: str = 'C',
        target_y: int = 400,
        target_time: float = 0.0,
        fall_duration: float = 2.0,
        chord: Optional[str] = None,
        fall_dur: Optional[float] = None
    ):
        self.note_id = note_id
        self.id = note_id  # Bug 11: Alias for backward compatibility
        self.string_index = string_index
        self.target_chord = chord if chord is not None else target_chord
        self.chord = self.target_chord
        self.target_y = target_y
        self.target_time = target_time
        self.fall_duration = fall_dur if fall_dur is not None else fall_duration
        self.spawn_time = target_time - self.fall_duration
        self.hit_status: Optional[str] = None  # 'PERFECT', 'GOOD', 'MISS'
        self.current_y = 0.0

    def update_position(self, current_time: float, spawn_y: int = 40) -> float:
        """Calculate current Y position based on linear time interpolation."""
        progress = (current_time - self.spawn_time) / self.fall_duration
        self.current_y = spawn_y + progress * (self.target_y - spawn_y)
        return self.current_y


class FloatingPopup:
    """Animated text popup for hit judgment (PERFECT, GOOD, MISS)."""

    def __init__(self, text: str, x: int, y: int, color: Tuple[int, int, int], duration: float = 0.50):
        self.text = text
        self.x = x
        self.y = y
        self.start_y = y
        self.color = color
        self.duration = duration
        self.spawn_time = time.time()
        self.alpha = 1.0

    def update(self) -> bool:
        """Returns True if popup is still alive, False if expired."""
        elapsed = time.time() - self.spawn_time
        if elapsed >= self.duration:
            return False
        # Float upward smoothly
        self.y = int(self.start_y - 40.0 * (elapsed / self.duration))
        # Fade out
        self.alpha = max(0.0, 1.0 - (elapsed / self.duration))
        return True


class RhythmManager:
    """
    Rhythm gameplay coordinator supporting Guitar Hero / Beat-Match mode.
    Handles note spawning according to song tempo, evaluates precision offsets,
    and maintains combo streaks with dynamic multipliers.
    """

    HIT_PERFECT_DIST = 24  # pixels tolerance for Perfect
    HIT_GOOD_DIST = 58     # pixels tolerance for Good
    MISS_DIST = 75         # note passed string without hit

    CHORDS_POOL = ['C', 'Dm', 'Em', 'G']

    def __init__(self, bpm: float = 105.0):
        self.bpm = bpm
        self.beat_interval = 60.0 / bpm
        self.is_active = False

        self.notes: List[RhythmNote] = []
        self.popups: List[FloatingPopup] = []
        self.next_note_id = 0
        self.last_spawn_beat_time = 0.0

        # Score & Combo stats
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.multiplier = 1
        self.perfect_count = 0
        self.good_count = 0
        self.miss_count = 0

    def toggle(self) -> bool:
        """Alias for toggle_mode."""
        return self.toggle_mode()

    def toggle_mode(self) -> bool:
        """Toggle between Free Play and Rhythm Game mode."""
        self.is_active = not self.is_active
        if self.is_active:
            self.reset()
            self.last_spawn_beat_time = time.time() + 1.0
        else:
            self.notes.clear()
            self.popups.clear()
        return self.is_active

    def reset(self):
        """Reset score and active note pool."""
        self.notes.clear()
        self.popups.clear()
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.multiplier = 1
        self.perfect_count = 0
        self.good_count = 0
        self.miss_count = 0

    def update(
        self,
        current_time: float,
        string_rects: List[Tuple[int, int, int, int]],
        spawn_y: int = 50
    ):
        """Update note trajectories, spawn beat notes, and prune expired targets."""
        # Always update floating popups so they fade away cleanly even on mode exit
        self.popups = [p for p in self.popups if p.update()]

        if not self.is_active or not string_rects:
            return

        # Spawn rhythmic notes on beat
        if current_time >= self.last_spawn_beat_time:
            str_idx = random.randint(0, len(string_rects) - 1)
            target_chord = random.choice(self.CHORDS_POOL)
            s_item = string_rects[str_idx]
            if isinstance(s_item[0], (tuple, list)):
                target_y = int((s_item[0][1] + s_item[1][1]) / 2)
            else:
                target_y = int((s_item[1] + s_item[3]) / 2)

            fall_dur = 1.8  # 1.8 seconds travel time
            new_note = RhythmNote(
                note_id=self.next_note_id,
                string_index=str_idx,
                target_chord=target_chord,
                target_y=target_y,
                target_time=current_time + fall_dur,
                fall_duration=fall_dur
            )
            self.notes.append(new_note)
            self.next_note_id += 1
            # Next beat interval (with slight syncopation: 1 or 2 beats)
            step_beats = random.choice([1.0, 1.0, 2.0])
            self.last_spawn_beat_time = current_time + (self.beat_interval * step_beats)

        # Update note positions & detect misses
        alive_notes = []
        for note in self.notes:
            if note.hit_status is not None:
                continue

            curr_y = note.update_position(current_time, spawn_y)

            # If note passed way below string target without hit -> Miss
            if curr_y > note.target_y + self.MISS_DIST:
                note.hit_status = 'MISS'
                if 0 <= note.string_index < len(string_rects):
                    self._handle_miss(string_rects[note.string_index])
            else:
                alive_notes.append(note)

        self.notes = alive_notes
        # Bug 12 Fix: Removed redundant second popup filter that was here before

    def check_hit(
        self,
        strum_event: dict,
        string_rects: Optional[list] = None
    ) -> Optional[str]:
        """
        Evaluate strum against falling notes on the strummed string.
        Returns judgment: 'PERFECT', 'GOOD', or None
        """
        if not self.is_active or not self.notes:
            return None

        str_idx = strum_event['string_index']
        strum_chord = strum_event['chord']
        strum_x = strum_event['strum_x']
        strum_y = strum_event['string_y']

        # Find closest note on this string
        candidates = [n for n in self.notes if n.string_index == str_idx and n.hit_status is None]
        if not candidates:
            return None

        # Sort by distance to string line
        closest_note = min(candidates, key=lambda n: abs(n.current_y - n.target_y))
        dist = abs(closest_note.current_y - closest_note.target_y)

        # Chord match check: bonus points if chord matches target chord, or half points
        chord_matches = (strum_chord == closest_note.target_chord)

        judgment = None
        if dist <= self.HIT_PERFECT_DIST:
            judgment = 'PERFECT'
            base_pts = 120 if chord_matches else 80
            self.score += base_pts * self.multiplier
            self.combo += 1
            self.perfect_count += 1
            color = (0, 255, 255)  # Cyan glow
        elif dist <= self.HIT_GOOD_DIST:
            judgment = 'GOOD'
            base_pts = 60 if chord_matches else 40
            self.score += base_pts * self.multiplier
            self.combo += 1
            self.good_count += 1
            color = (0, 255, 120)  # Emerald green glow
        else:
            return None

        # Update combo multiplier
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        self.multiplier = min(4, 1 + (self.combo // 5))

        closest_note.hit_status = judgment

        # Spawn popup text
        popup_text = f"{judgment}! +{base_pts * self.multiplier}"
        if self.combo > 1 and self.combo % 5 == 0:
            popup_text += f" (x{self.multiplier})"

        self.popups.append(FloatingPopup(
            text=popup_text,
            x=strum_x - 30,
            y=strum_y - 25,
            color=color
        ))
        return judgment

    def _handle_miss(self, str_rect):
        """Handle missed note: reset combo streak and spawn MISS popup."""
        self.miss_count += 1
        self.combo = 0
        self.multiplier = 1

        if isinstance(str_rect[0], (tuple, list)):
            mid_x = int((str_rect[0][0] + str_rect[1][0]) / 2)
            mid_y = int((str_rect[0][1] + str_rect[1][1]) / 2)
        else:
            mid_x = int((str_rect[0] + str_rect[2]) / 2)
            mid_y = int((str_rect[1] + str_rect[3]) / 2)

        self.popups.append(FloatingPopup(
            text="MISS!",
            x=mid_x - 20,
            y=mid_y,
            color=(0, 0, 255)  # Red
        ))

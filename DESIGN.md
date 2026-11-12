# DESIGN — AgriScanner UI (v3.0 Dark Nature)

## Principles
- **Immersive Organic Theme**: A deep forest-inspired dark mode that reduces eye strain and emphasizes plant health data.
- **Glassmorphism**: Semi-transparent surfaces with background blur to create depth and modern aesthetics.
- **High-Contrast Data**: Critical diagnosis information uses vibrant greens and whites against dark backgrounds for maximum readability in the field.

## Page layout (Streamlit Wide Mode)
1. **Sidebar (Deep Forest)**:
   - Modern branding with custom iconography.
   - Glass-styled info boxes for usage guidance.
   - Live system status (Model Ready).
2. **Glassmorphism Header**:
   - Floating card effect with a glowing text gradient (Leaf Green to Emerald).
3. **Environmental Context**:
   - Dark translucent cards with vibrant typography for Weather, Humidity, and Rainfall.
   - Interactive hover states for a tactile feel.
4. **Diagnosis Interface**:
   - Themed tabs with neon-green active states.
   - **Result Section**:
     - **Left Column**: Leaf image preview + glowing risk alerts.
     - **Right Column**: 
       - `result-container` with an inset shadow and glass effect.
       - Glowing confidence badges and severity pills.
       - Minimalist progress bars for top predictions.
5. **AI Doctor's Prescription**:
   - Large glassmorphic container with high line-height for readability of treatment plans.

## Visual Style
- **Typography**: `Inter` Google Font (Weights 400-800) for a robust, readable look.
- **Palette**: 
  - Background: Radial gradient (`#0a1f0a` to `#040d04`)
  - Accent Green: `#4caf50` (Vibrant) / `#81c784` (Soft)
  - Text: `#e0f2f1` (Mint White) / `#ffffff` (Pure White)
  - Surfaces: `rgba(255, 255, 255, 0.03)` with `blur(10px)`
- **Components**:
  - Buttons: Solid forest green with glowing hover effects.
  - Cards: 24px corner radius with thin borders (`rgba(255, 255, 255, 0.05)`).

## States
- **Idle**: Deep green aesthetic with soft ambient glowing elements.
- **Scanning**: Pulsing themed spinners.
- **Success**: Vibrant emerald highlights for healthy results.
- **Warning**: High-contrast alerts with red/amber accents that pop against the dark theme.

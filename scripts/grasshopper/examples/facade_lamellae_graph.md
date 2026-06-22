# Facade Lamellae — Native GH Graph

Fully native Grasshopper graph (no C# script). Built programmatically via
`run_python` using `GH_ComponentParamServer` wiring.

## Sliders
| NickName   | Min  | Default | Max  |
|------------|------|---------|------|
| FacadeW    | 2    | 20      | 50   |
| FacadeH    | 1    | 10      | 30   |
| LamCount   | 3    | 20      | 100  |
| LamDepth   | 0.05 | 0.3     | 1.0  |
| LamAngle   | -80  | 30      | 80   |

## Component chain
```
FacadeW, LamCount → Division → spacing
spacing, LamCount → Series  → XPositions (list)
XPositions        → ConstructPoint(x,0,0) → StartPts

LamAngle          → Radians → rad
rad               → Sine    → sinA
rad               → Cosine  → cosA
sinA × LamDepth   → Multiplication → dx
cosA × LamDepth   → Multiplication → dy
UnitX × dx        → Amplitude → VecX
UnitY × dy        → Amplitude → VecY
VecX + VecY       → Addition(Vector) → FinVec

StartPts + FinVec → Move → EndPts
StartPts, EndPts  → Line → FinLines
UnitZ × FacadeH   → Amplitude → HeightVec
FinLines, HeightVec → Extrude → FinSurfs   ← main output

ConstPt(0,0,0), ConstPt(FacadeW,0,0) → Line → WallBase
WallBase, HeightVec → Extrude → WallSurf   ← backing wall
```

## GUIDs used
| Component      | GUID                                   |
|----------------|----------------------------------------|
| Division       | 9c85271f-89fa-4e9f-9f4a-d75802120ccc  |
| Series         | e64c5fb1-845c-4ab1-8911-5f338516ba67  |
| ConstructPt    | 3581f42a-9592-4549-bd6b-1c0fc39d067b  |
| Radians        | a4cd2751-414d-42ec-8916-476ebf62d7fe  |
| Sine           | 7663efbb-d9b8-4c6a-a0da-c3750a7bbe77  |
| Cosine         | d2d2a900-780c-4d58-9a35-1f9d8d35df6f  |
| Multiplication | b8963bb1-aa57-476e-a20e-ed6cf635a49c  |
| Unit X         | 79f9fbb3-8f1d-4d9a-88a9-f7961b1012cd  |
| Unit Y         | d3d195ea-2d59-4ffa-90b1-8b7ff3369f69  |
| Unit Z         | 9103c240-a6a9-4223-9b42-dbd19bf38e2b  |
| Amplitude      | 6ec39468-dae7-4ffa-a766-f2ab22a2c62e  |
| Addition(Vec)  | fb012ef9-4734-4049-84a0-b92b85bb09da  |
| Move           | b40f28a2-ba30-4ac2-afe5-a6ece7f985fc  |
| Line           | 4c4e56eb-2f04-43f9-95a3-cc46a14f495a  |
| Extrude        | 962034e9-cc27-4394-afc4-5c16e3447cf9  |

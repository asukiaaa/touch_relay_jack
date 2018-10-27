# This is a CadQuery script template
# Add your script code below
import cadquery as cq
from Helpers import show

clealance = 0.2
boxInnerWidth = 34.0
boxInnerLength = 39.5
boxInnerHighHeight = 20.0
boxInnerLowHeight = 4.0
boxThickness = 1.5
boxFillet = 1.5
boxOuterWidth = boxInnerWidth + boxThickness * 2
boxOuterLength = boxInnerLength + boxThickness * 2
boxOuterHeight = boxInnerHighHeight + boxThickness * 2
boxTopSpaceLength = 20.5
mountingHoleRadius = 3.0 / 2
mountingHolePositions = [(0, 12.2), (-13.0, -16.8), (13.0, -16.8)]
mountHeight = 2.0
coverHoleRadius = 3.5 / 2
coverHolePositions = mountingHolePositions[1:]
jackHoleRadius = 6.0 / 2
jackCenterHeight = 4.0 + mountHeight
jackCenterFromPCBCenter = 11.0
usbHoleWidth = 10.0
usbHoleHeight = 5.0
usbHoleCenterHeight = 15 + mountHeight
usbHoleCenterFromPCBCenter = jackCenterFromPCBCenter
hookWidth = 6.0
hookHeight = 1.5
hookLength = boxThickness * 2 / 3
hookConnectionLength = 1.0
hookCenterXFromPCBCenter = 9.0
hookCenterHeight = 16.5 + hookHeight / 2 + mountHeight
M4HoleFromPCBCenter = 13.5
M4HoleRadius = 9.0 / 2
LEDSpaceWidth = 4.0
LEDSpaceLength = 5.0
LEDSpaceHeight = 0.5
LEDSpaceCenterFromPCBCenter = 1.0

body = cq.Workplane("XY").box(boxOuterWidth, boxOuterLength, boxOuterHeight)\
    .translate((0, 0, boxOuterHeight/2 - boxThickness))
topSpaceHeight = boxInnerHighHeight + boxThickness - boxInnerLowHeight
topSpace = cq.Workplane("XY")\
    .box(boxOuterWidth,
         boxTopSpaceLength + boxThickness,
         topSpaceHeight)\
    .translate(
        (0,
         - boxOuterLength / 2 + (boxTopSpaceLength + boxThickness) / 2,
         boxInnerLowHeight + boxThickness + topSpaceHeight / 2))
body = body.cut(topSpace)\
    .edges("|X or |Y or |Z").fillet(boxFillet)

inner = cq.Workplane("XY").box(boxInnerWidth,
                               boxInnerLength,
                               boxInnerHighHeight + boxThickness)\
    .translate((0, 0, (boxInnerHighHeight + boxThickness) / 2))
body = body.cut(inner)

mount = cq.Workplane("XY").circle(mountingHoleRadius + 1).extrude(mountHeight)
holeHeight = mountHeight + boxThickness
hole = cq.Workplane("XY").circle(mountingHoleRadius)\
    .extrude(holeHeight)
for (x, y) in mountingHolePositions:
    body = body.union(mount.translate((x, y, 0)))\
        .cut(hole.translate((x, y, -boxThickness)))

jackHole = cq.Workplane("YZ").move(jackCenterFromPCBCenter, jackCenterHeight)\
    .circle(jackHoleRadius).extrude(-boxThickness)\
    .translate((-boxInnerWidth/2, 0, 0))
body.cut(jackHole)

usbHole = cq.Workplane("YZ")\
    .move(usbHoleCenterFromPCBCenter, usbHoleCenterHeight)\
    .box(usbHoleWidth, usbHoleHeight, boxThickness)\
    .translate((-boxInnerWidth/2 - boxThickness/2, 0, 0))
body.cut(usbHole)

coverPoints = [
    (boxInnerHighHeight + boxThickness, boxInnerLength / 2 - clealance),
    (boxInnerHighHeight + boxThickness,
     - boxInnerLength / 2 + boxTopSpaceLength),
    (boxInnerLowHeight + boxThickness,
     - boxInnerLength / 2 + boxTopSpaceLength),
    (boxInnerLowHeight + boxThickness, - boxInnerLength / 2 + clealance),
    (boxInnerLowHeight, - boxInnerLength / 2 + clealance),
    (boxInnerLowHeight,
     - boxInnerLength / 2 + boxTopSpaceLength + boxThickness),
    (boxInnerHighHeight,
     - boxInnerLength / 2 + boxTopSpaceLength + boxThickness),
    (boxInnerHighHeight, boxInnerLength / 2 - clealance)]
coverWidth = boxInnerWidth - clealance * 2
cover = cq.Workplane("ZY").moveTo(*coverPoints[0]).polyline(coverPoints[1:])\
    .close().extrude(coverWidth)\
    .translate((coverWidth / 2, 0, 0))\
    .edges("not(>Y or <Y or |Z or |Y)").fillet(boxFillet)

hookSpace = cq.Workplane("XY").box(hookWidth + clealance * 2,
                                   boxThickness,
                                   hookHeight + clealance * 2)
hook = cq.Workplane("XY").box(hookWidth,
                              hookLength + hookConnectionLength,
                              hookHeight)\
    .edges(">Y and <Z").fillet(hookHeight * 2 / 3)
for x in [hookCenterXFromPCBCenter, - hookCenterXFromPCBCenter]:
    body.cut(hookSpace.translate((x,
                                  boxInnerLength/2 + boxThickness / 2,
                                  hookCenterHeight)))
    cover = cover.union(hook.translate(
        (x,
         boxInnerLength/2 + (hookLength + hookConnectionLength)/2 -
         hookConnectionLength,
         hookCenterHeight)))

coverHole = cq.Workplane("XY").circle(coverHoleRadius).extrude(boxThickness)
for (x, y) in coverHolePositions:
    cover.cut(coverHole.translate((x, y, boxInnerLowHeight)))

M4Hole = cq.Workplane("XY").circle(M4HoleRadius).extrude(boxThickness)\
    .translate((0, -M4HoleFromPCBCenter, boxInnerLowHeight))
cover.cut(M4Hole)

LEDSpace = cq.Workplane("XY")\
    .box(LEDSpaceLength, LEDSpaceLength, LEDSpaceHeight)\
    .translate((boxInnerWidth / 2 - LEDSpaceWidth / 2,
                -LEDSpaceCenterFromPCBCenter,
                boxInnerLowHeight + LEDSpaceHeight / 2))
cover.cut(LEDSpace)

show(cover)
show(body)

use <MCAD/boxes.scad>

/* [Hidden] */
mPlateH=2;
mStandoffH=5;

/* [Base Plate] */
plateW = 95;
plateL = 195;
plateH = 5;

/* [Standoff Height] */
rPiStandoffH = 3;
BBBlueStandoffH = 3;

/* [Pin Spacing] */
front_Pin_Spacing=12.5; // /*[5:40]*/
rear_Pin_Spacing=12.5;  // /*[5:40]*/

/* [Pin Positioning] */
front_Pin_Position=85; // /*[73:90]*/
rear_Pin_Position=90; // /*[73:90]*/

/* [rPi Mount rotation] */
rot_angle = 0;  // [0,90,-90]

print_part();

module print_part() {
    
    difference() {
        
        // Set up the solid parts of the base plate and create a union
        // to perform the difference
        union(){
            
            // BASE PLATE
            newPlate(plateH);
            
            // BB Blue in forward position
            //translate([-19, 0, 8.5]) beagleBoneBlue();
            // BB Blue in back position
            //translate([7.25, 0, 8.5]) beagleBoneBlue();
            
            //translate([-21, 0, 8.5]) raspberryPi();
            
            // Raspberry Pi Pins
            color("Red")
            if ( rot_angle == 0 ) {
                translate([0,0,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    rPiMountPins(plateH, rPiStandoffH);
            }
            else if ( rot_angle == 90 ) {
                translate([-15,3,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    rPiMountPins(plateH, rPiStandoffH);
            }
            else if ( rot_angle == -90 ) {
                translate([-15,-5,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    rPiMountPins(plateH, rPiStandoffH);
            }
            
            // BeagleBone Blue Mount Pins forward position
            /*
            color("Blue")
            if ( rot_angle == 0 ) {
                translate([0,0,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    BBBlueUSBFwdMountPins(plateH, BBBlueStandoffH);
            }
            else if ( rot_angle == 90 ) {
                translate([-15,3,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    BBBlueUSBFwdMountPins(plateH, BBBlueStandoffH);
            }
            else if ( rot_angle == -90 ) {
                translate([-15,-5,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    BBBlueUSBFwdMountPins(plateH, BBBlueStandoffH);
            }
            */
            
            // BeagleBone Blue Mount Pins - rear position
            color("Blue")
            translate([26.25, 0, 0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                    BBBlueUSBFwdMountPins(plateH, BBBlueStandoffH);
            
            // PWM Driver Mount Pins
            translate([-3.0,0,0]) 
                PwmDvrMountPins(plateH, rPiStandoffH);
        }
      
        // Now remove all of the holes using the difference
        
        // Raspberry Pi mount pin holes
        if ( rot_angle == 0 ) {
            translate([0,0,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #rPiHoles();
        }
        else if ( rot_angle == 90 ) {
            translate([-15,3,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #rPiHoles();
        }
        else if ( rot_angle == -90 ) {
            translate([-15,-5,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #rPiHoles();
        }
        
        // BeagleBone Blue mount pin holes - forward position
        /*
        if ( rot_angle == 0 ) {
            translate([0,0,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #BBBlueUSBFwdHoles();
        }
        else if ( rot_angle == 90 ) {
            translate([-15,3,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #BBBlueUSBFwdHoles();
        }
        else if ( rot_angle == -90 ) {
            translate([-15,-5,0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #BBBlueUSBFwdHoles();
        }
        */
        
        // BeagleBone Blue Mount Pin holes shifted back
        translate([26.25, 0, 0]) rotate([0,0,rot_angle]) translate([-3.0,0,0]) 
                #BBBlueUSBFwdHoles();
        
        // BeagleBone Blue coil cutout
        
        // Forward position
        //beagleBoneBlueCoilCutouts();
        //*mirror([0,1,0]) beagleBoneBlueCoilCutouts();
        
        // Rear position
        translate([26.25, 0, 0]) beagleBoneBlueCoilCutouts();
        mirror([0,1,0]) translate([26.25, 0, 0]) beagleBoneBlueCoilCutouts();
        
        // PWM Driver holes
        translate([-3.0, 0, 0])
            #PwmDvrHoles();
        
        // Roll cage handle mounting holes
        #handleMountingHoles();
        
        // Cutouts for cotter pins 
        #platePinClearance(front_Pin_Spacing, rear_Pin_Spacing);
        
        // Holes to mount to chassis 
        #translate([-3, 0, 0])
            plateMountHolesPins(front_Pin_Spacing, rear_Pin_Spacing, front_Pin_Position, rear_Pin_Position);
        
        // Wire harness holes
        #wireHarnessHoles();
        translate([-90, 0, 0])
            #wireHarnessHoles();
        
      }  
}


/*
 * COMPONENT MODULES
 */

module newPlate (plateH=5, plateW=95, plateL=195) {
    translate([0,0,plateH/2])  //translate([3,0,plateH/2])
    //cube([plateL,plateW,plateH],center=true);
        roundedBox([plateL,plateW,plateH],15, true);   
}

module raspberryPi() {
    $fn=32;
    piL = 85;
    piW = 56;
    piH = 1.5;
    
    rearHoleX = piL/2 - 3.5;
    frontHoleX = rearHoleX - 58;
    
    surfaceMountH = 1.5;
    
    difference() {
        union() {
            
            // Base
            #color("IndianRed")
                roundedBox([piL, piW, piH], 3, true);
            
            // Surface mount thingies
            
            // Audio Jack mount
            color("Silver")
            translate([frontHoleX + 4, piW/2 - 10, -piH/2 -surfaceMountH])
                cube([8,10,surfaceMountH]);
            
            // GPIO mount
            color("Silver")
            translate([frontHoleX + 3.5, -piW/2 + 1, -piH/2 -surfaceMountH])
                cube([50.5,5,surfaceMountH]);
            
            // USB mount
            color("Silver")
            translate([frontHoleX - 16, -piW/2 + 1, -piH/2 -surfaceMountH])
                cube([8, 14, surfaceMountH]);
        }
    
        // Mount Holes
        
        // Front
        translate([frontHoleX, -piW/2 + 3.5, -4]) 
            #cylinder(r=1.3, h=14, center=true);
        translate([frontHoleX, piW/2 - 3.5, -4]) 
            #cylinder(r=1.3, h=14, center=true);
    
        // Rear
        translate([rearHoleX, -piW/2 + 3.5, -4]) 
            #cylinder(r=1.3, h=14, center=true);
        translate([rearHoleX, piW/2 - 3.5, -4]) 
            #cylinder(r=1.3, h=14, center=true);
    }
}

module beagleBoneBlue () {
    
    $fn=32;
    bbbL = 86;
    bbbW = 54;
    bbbH = 1.5;
    
    coilH = 4;
    surfaceMountH = 1;
    
    difference() {
        union() {
        
            // Substrate
            #color("SteelBlue")
            hull() {
                // Front
                translate([-bbbL/4, 0, 0])
                    roundedBox([bbbL/2, bbbW, bbbH], 5, true);
                // Rear
                translate([bbbL/4, 0, 0])
                    roundedBox([bbbL/2, bbbW, bbbH], 10, true);
            }
            
            // USB
            color("Silver")
            translate([-bbbL/2 - 2, -bbbW/2 + 2, bbbH/2])
                cube([13.5, 12, 6]);
            
            // Coils
            
            // 3R6 M3
            color("Black")
            translate([bbbL/2 - 29, bbbW/2 - 10, -bbbH/2 - coilH])
                cube([8,8,coilH]);
            
            // 6R3 (middle)
            color("Black")
            translate([bbbL/2 - 41.5, bbbW/2 - 7, -bbbH/2 - coilH])
                cube([6,5,coilH]);
            
            // 6R3 (front)
            color("Black")
            translate([-bbbL/2 + 19, bbbW/2 - 10, -bbbH/2 - coilH])
                cube([6,5,coilH]);
            
            
            // Surface mount thingies
            
            color("Silver")
            translate([bbbL/2 - 35.25, bbbW/2 - 12, -bbbH/2 - surfaceMountH])
                cube([6,10,surfaceMountH]);
        }
        
        // Mount Holes
        
        // Front
        translate([-bbbL/2 + 14, -bbbW/2 + 3, -4]) 
            #cylinder(r=1.35, h=14, center=true);
        translate([-bbbL/2 + 14, bbbW/2 - 3, -4]) 
            #cylinder(r=1.35, h=14, center=true);
    
        // Rear
        translate([bbbL/2 - 6, -bbbW/2 + 6, -4]) 
            #cylinder(r=1.35, h=14, center=true);
        translate([bbbL/2 - 6, bbbW/2 - 6, -4]) 
            #cylinder(r=1.35, h=14, center=true);
    }

}

module beagleBoneBlueCoilCutouts() {
    translate([-40, 19.5, 2.5])
        #roundedBox([8, 8, plateH + 2*rPiStandoffH], 1, true);
    translate([-15, 21.5, 2.5])
        #roundedBox([8, 8, plateH + 2*rPiStandoffH ], 1, true);
    translate([-1, 21, 2.5])
        #roundedBox([9, 9, plateH + 2*rPiStandoffH], 1, true); 
}

module wireHarnessHoles() {
    hull() {
        wireHoleOriginal(10, 8, 8);
        translate([30,0,0])
            wireHoleOriginal(10, 8, 8);
        //wireHole(10, 32, 8);        
    }    
}

/* UNUSED
module rPiMounts(rotation=0) {
    if ( rotation==0 ) {
        difference() {
            translate([-3.0,0,0])
                rPiMountPins(plateH,3);
            translate([-3.0,0,0])
                #rPiHoles();
        }
    }
    if ( rotation==90 ) {
        difference() {
            rotate([0,0,rotation]) translate([-3.0,0,0])
                rPiMountPins(plateH,3);
            rotate([0,0,rotation]) translate([-3.0,0,0])
                #rPiHoles();
        }
    }  
}
*/

/*
Holes for mounting the roll cage handle 
*/
module handleMountingHoles(plateh=3) {
    $fn=30;
    platePinW=3.1; // actual mount hole diameter
    plateH=15.0;
    platePinH=plateh;
    
    // Front Right
    translate([-66.9, -42.35, plateh])
        cylinder(r=platePinW/2, h=platePinH*5, center=true);
    
    // Front Left
    translate([-66.9, 42.35, plateh])
        cylinder(r=platePinW/2, h=platePinH*5, center=true);
    
    // Tail
    translate([90.8, 0, plateh])
        cylinder(r=platePinW/2, h=platePinH*5, center=true);    
}

/*
 * BeagleBoard Blue hole spacing:
 *   USB to quadrature end: 66mm spacing (45 + 21)
 *   USB end pins: 48mm (24 + 24)
 *   Quadrature pins: 42mm (22 + 22)
*/

module BBBlueUSBFwdMountPins (plateH=5, piOffset=5) {
    $fn=20;
    platePinW = 5.4;
    platePinH = plateH + piOffset;
    
    // Rear Mounts
    translate([21, -21.0, platePinH/2]) 
        cylinder(r=platePinW/2, h=platePinH, center=true);
    translate([21, 21.0, platePinH/2])
        cylinder(r=platePinW/2, h=platePinH, center=true);
    
    // Front Mounts
    //translate([-45, -24.0, platePinH/2])
    //    cylinder(r=platePinW/2, h=platePinH, center=true);
    translate([-45, 24.0, platePinH/2])
        cylinder(r=platePinW/2, h=platePinH, center=true);    
}

module BBBlueUSBFwdHoles () {
    $fn=30;
    platePinW=2.7; // actual mount hole diameter
    plateH=15.0;
    platePinH = plateH;
    
    // Rear Holes
    translate([21, -21.0, 0]) 
        cylinder(r=platePinW/2, h=plateH*2, center=true);
    translate([21, 21.0, 0]) rotate([0, 0, 90]) 
        cylinder(r=platePinW/2, h=plateH*2, center=true);
    
    // Front Holes
    translate([-45, -24.0, 0]) rotate([0, 0, 90])
        cylinder(r=platePinW/2, h=plateH*2, center=true);
    translate([-45, 24.0, 0]) rotate([0, 0, 90])
        cylinder(r=platePinW/2, h=plateH*2, center=true); 
}

/* UNUSED
module BBBlueUSBBwdHoles () {
    $fn=30;
    platePinW=2.7; // actual mount hole diameter
    plateH=15.0;
    platePinH=plateH;
    
    translate([21,-24.0,0]) cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([21,24.0,0]) rotate([0,0,90]) cylinder(r=platePinW/2,h=plateH*2,center=true);
    //end 2
    translate([-45,-21.0,0]) rotate([0,0,90])cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([-45,21.0,0]) rotate([0,0,90])cylinder(r=platePinW/2,h=plateH*2,center=true); 
}

module rBBBlueUSBBwdMountPins (plateH=5,piOffset=2) {
    $fn=20;
    platePinW=5.8;
    platePinH=plateH+piOffset;
translate([21,-24.0,platePinH/2]) cylinder(r=platePinW/2,h=platePinH,center=true);
translate([21,24.0,platePinH/2]) rotate([0,0,90]) cylinder(r=platePinW/2,h=platePinH,center=true);
//end 2
translate([-45,-21.0,platePinH/2]) rotate([0,0,90])cylinder(r=platePinW/2,h=platePinH,center=true);
translate([-45,21.0,platePinH/2]) rotate([0,0,90])cylinder(r=platePinW/2,h=platePinH,center=true);    
}
*/

module rPiHoles () {
    $fn=30;
    platePinW=2.7; // actual mount hole diameter
    plateH=15.0;
    platePinH=plateH;
    
    // Rear
    translate([21,-24.5,0]) cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([21,24.5,0]) rotate([0,0,90]) cylinder(r=platePinW/2,h=plateH*2,center=true);
    
    // Front
    translate([-37,-24.5,0]) rotate([0,0,90])cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([-37,24.5,0]) rotate([0,0,90])cylinder(r=platePinW/2,h=plateH*2,center=true);    
}

module rPiMountPins (plateH=5,piOffset=2) {
    $fn=20;
    platePinW = 5.4;
    platePinH = plateH + piOffset;
    
    // Rear
    translate([21,-24.5,platePinH/2]) cylinder(r=platePinW/2,h=platePinH,center=true);
    //translate([21,24.5,platePinH/2]) rotate([0,0,90]) cylinder(r=platePinW/2,h=platePinH,center=true);
    
    // Front
    translate([-37,-24.5,platePinH/2]) rotate([0,0,90])cylinder(r=platePinW/2,h=platePinH,center=true);
    translate([-37,24.5,platePinH/2]) rotate([0,0,90])cylinder(r=platePinW/2,h=platePinH,center=true);    
}


/*
 * PWM Driver mounts
 */
module PwmDvrMountPins (plateH=5,piOffset=2) {
    $fn=20;
    platePinW=5.8;
    platePinH=plateH+piOffset;

    translate([74,-28,platePinH/2]) 
        cylinder(r=platePinW/2,h=platePinH,center=true);
    translate([74,28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH,center=true);
    
    //end 2
    translate([55,-28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH,center=true);
    translate([55,28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH,center=true);    
}

/*
 * PWM Driver holes
 */
module PwmDvrHoles (plateH=5,piOffset=2) {
    $fn=30;
    platePinW = 2.7;
    platePinH = plateH + piOffset;
    
    translate([74,-28,platePinH/2]) 
        cylinder(r=platePinW/2,h=platePinH*2,center=true);
    translate([74,28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH*2,center=true);
    //end 2
    translate([55,-28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH*2,center=true);
    translate([55,28,platePinH/2])
        cylinder(r=platePinW/2,h=platePinH*2,center=true);    
}

/* 
 * Cutouts for cotter pins
 */
module platePinClearance(fSpacing=12.5,rSpacing=12.5,fPos=85,rPos=90) {
    platePinH=3.0;
    plateH=5.0;
    pinSlotW=10;
    pinSlotL=25;
    
    //end 1 = Rear    
    translate([rPos-5,-rSpacing,plateH-(plateH-platePinH)/2]) 
        cube([pinSlotL,pinSlotW,plateH-platePinH],center=true);
    translate([rPos-5,rSpacing,plateH-(plateH-platePinH)/2]) 
        cube([pinSlotL,pinSlotW,plateH-platePinH],center=true);
    
    //end 2 - Front
    translate([-fPos,-fSpacing,plateH-(plateH-platePinH)/2]) 
        cube([pinSlotL,pinSlotW,plateH-platePinH],center=true);
    translate([-fPos,fSpacing,plateH-(plateH-platePinH)/2]) 
        cube([pinSlotL,pinSlotW,plateH-platePinH],center=true);
}

/*
 * Holes to mount to chassis
 */
module plateMountHolesPins(fSpacing=12.5,rSpacing=12.5,fPos=85,rPos=85) {
    $fn=6;
    platePinW=5.8;
    plateH=5.0;
    platePinH=plateH;
    pinSlotW=10;
    pinSlotL=25;
    
    //end 1 - Rear    
    translate([rPos,-rSpacing,plateH-(plateH-platePinH)/2]) 
        cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([rPos,rSpacing,plateH-(plateH-platePinH)/2]) 
        cylinder(r=platePinW/2,h=plateH*2,center=true);
    
    //end 2 - Front
    translate([-fPos,-fSpacing,plateH-(plateH-platePinH)/2]) 
        cylinder(r=platePinW/2,h=plateH*2,center=true);
    translate([-fPos,fSpacing,plateH-(plateH-platePinH)/2]) 
        cylinder(r=platePinW/2,h=plateH*2,center=true);   
}

module wireHoleOriginal( defH=3.0, defW=26, defR=8) {
    $fn=50;

    translate([30, 0, -defH/4])
    linear_extrude(height = defH, center = false, convexity = 100, scale=[1,1], $fn=20, twist=0)
        hull() {
          translate([0, -defW/2, 0]) circle(defR);
          translate([0, defW/2, 0]) circle(defR);
        }
}

module wireHole( defH=3.0, defW=26, defR=8 ) {
    $fn=50;

    translate([30, 0, -defH/4])
    rotate([0, 0, 270])
    linear_extrude(height = defH, center = false, convexity = 100, scale=[1,1], $fn=20, twist=0)
        hull() {
          translate([0, defW, 0]) circle(defR);
          translate([0, 0, 0]) circle(defR);
        }
}

import G4Interface

def test_01_box() :
    b = G4Interface.Box("b",10,10,10)

    l = G4Interface.Logical("l",b)

    p1 = G4Interface.Placement("p1",l,(0,0,0),(30,0,0))
    p2 = G4Interface.Placement("p2",l,(0,0,45),(00,0,0))
    p3 = G4Interface.Placement("p3",l,(0,0,0),(-30,0,0))

    bw = G4Interface.Box("world",50,50,50)
    bw.set_colour((0,0,1))
    bw.set_alpha(0.15)

    lw = G4Interface.Logical("lw",bw, pvs=[p1,p2,p3])
    lw.stage.Export("./test_01_box.usda")
from pxr import Usd, UsdGeom, Gf, Sdf, G4

class SetColorAlphaMixin :
    def set_colour(self, colour = (1,1,1)):
        self.prim.CreateDisplayColorAttr([Gf.Vec3f(*colour)])

    def set_alpha(self, alpha = 1.0):
        self.prim.CreateDisplayOpacityAttr([alpha])

class Box(SetColorAlphaMixin) :
    def __init__(self, name="box", x=100, y=100.0, z=100.0):

        self.name = name
        self.x = x
        self.y = y
        self.z = z

        self.stage = Usd.Stage.CreateInMemory()
        self.prim = G4.Box.Define(self.stage,"/"+self.name)
        self.prim.InstallUpdateListener()
        self.prim.GetXAttr().Set(self.x)
        self.prim.GetYAttr().Set(self.y)
        self.prim.GetZAttr().Set(self.z)

class Logical:
    def __init__(self, name, solid, pvs=[], material=None):
        self.name = name
        self.solid = solid
        self.material = material
        self.placements = pvs

        self.stage = Usd.Stage.CreateInMemory()
        self.prim = G4.Logical.Define(self.stage,"/"+name)
        self.prim.GetSolidprimAttr().Set(solid.name)
        self.prim.GetDaughtersAttr().Set([pv.name for pv in pvs])

        # Copy solid
        Sdf.CopySpec(solid.stage.GetRootLayer(), Sdf.Path("/"+solid.name),
                     self.stage.GetRootLayer(), Sdf.Path("/"+self.name+"/"+solid.name))

        # Copy PVs
        for pv in pvs :
            Sdf.CopySpec(pv.stage.GetRootLayer(), Sdf.Path("/"+pv.name),
                         self.stage.GetRootLayer(), Sdf.Path("/"+self.name+"/"+pv.name))

class Placement:
    def __init__(self, name, logical, rot = (0,0,0), tra = (0,0,0)) :
        self.name = name
        self.logical = logical
        self.rot = rot
        self.tra = tra

        self.stage = Usd.Stage.CreateInMemory()
        self.prim = G4.Placement.Define(self.stage,"/"+name)
        self.prim.InstallUpdateListener()
        self.prim.GetLogicalprimAttr().Set(logical.name)
        self.prim.GetRotationAttr().Set(self.rot)
        self.prim.GetTranslationAttr().Set(self.tra)

        # Copy logical
        Sdf.CopySpec(logical.stage.GetRootLayer(), Sdf.Path("/"+logical.name),
                     self.stage.GetRootLayer(), Sdf.Path("/"+self.name+"/"+logical.name))


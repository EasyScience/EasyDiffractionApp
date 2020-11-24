__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from PySide2.QtCore import QObject, Slot, qDebug
import numpy as np
import vtk


import random

def get_random_color(pastel_factor = 0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

def color_distance(c1,c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

def generate_new_color(existing_colors,pastel_factor = 0.5):
    max_distance = None
    best_color = None
    for i in range(0,100):
        color = get_random_color(pastel_factor = pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color,c) for c in existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


class VTKcanvasHandler(QObject):

    def __init__(self, parent=None):
        super(VTKcanvasHandler, self).__init__(parent=parent)
        self.fbo = None
        self.context = None
        self.actors = []
        self.max_distance = 2
        self.show_bonds = True

    @Slot()
    def clearScene(self):
        for actor in self.actors:
            self.fbo.removeActor(actor, update=False)
        self.actors = []
        self.fbo.update()

    @Slot()
    def create_plot_system(self):
        class system:
            def __init__(self):
                self.atoms = [[0, 0, 0],
                              [0, 0, 1],
                              [0, 1, 0],
                              [0, 1, 1],
                              [1, 0, 0],
                              [1, 0, 1],
                              [1, 1, 0],
                              [1, 1, 1],
                              ]
                self.lattice = [15, 15, 15, 90, 90, 90]
        if self.actors:
            qDebug('Lattice already drawn')
            return

        this_system = system()
        self.plot_system(this_system)
        qDebug('Lattice drawn')

    def plot_system2(self, crystal):
        lattice_actors = self.create_lattice2(crystal.cell)
        atom_actors = self.create_atoms2(crystal)
        if self.show_bonds:
            bond_actors = self.plot_bonds(crystal)
            self.actors = [*lattice_actors, *bond_actors, *atom_actors]
        else:
            self.actors = [*lattice_actors, *atom_actors]
        self.fbo.addActors(self.actors)
        Xmin = np.Inf
        Xmax = -np.Inf
        Ymin = np.Inf
        Ymax = -np.Inf
        Zmin = np.Inf
        Zmax = -np.Inf
        for actor in self.actors:
            (thisXmin, thisXmax, thisYmin, thisYmax, thisZmin, thisZmax) = actor.GetBounds()
            if thisXmin < Xmin:
                Xmin = thisXmin
            if thisXmax > Xmax:
                Xmax = thisXmax
            if thisYmin < Ymin:
                Ymin = thisYmin
            if thisYmax > Ymax:
                Ymax = thisYmax
            if thisZmin < Zmin:
                Zmin = thisZmin
            if thisZmax > Zmax:
                Zmax = thisZmax
        camera = self.fbo.getCamera()
        camera.SetPosition(4*Zmax, 7*Ymax, 4*Zmax)
        self.fbo.update()

    def plot_system(self, system):
        lattice_actors = self.create_lattice(system.lattice)
        atom_actors = self.create_atoms(system)
        self.actors = [*lattice_actors, *atom_actors]
        self.fbo.addActors(self.actors)
        Xmin = np.Inf
        Xmax = -np.Inf
        Ymin = np.Inf
        Ymax = -np.Inf
        Zmin = np.Inf
        Zmax = -np.Inf
        for actor in self.actors:
            (thisXmin, thisXmax, thisYmin, thisYmax, thisZmin, thisZmax) = actor.GetBounds()
            if thisXmin < Xmin:
                Xmin = thisXmin
            if thisXmax > Xmax:
                Xmax = thisXmax
            if thisYmin < Ymin:
                Ymin = thisYmin
            if thisYmax > Ymax:
                Ymax = thisYmax
            if thisZmin < Zmin:
                Zmin = thisZmin
            if thisZmax > Zmax:
                Zmax = thisZmax
        camera = self.fbo.getCamera()
        camera.SetPosition(4*Zmax, 7*Ymax, 4*Zmax)
        self.fbo.update()
        # trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])*system.lattice[0:3]  # This will be a property of the lattice.
        # self.fbo.setFocalPoint(trans_matrix.dot([0.5, 0.5, 0.5]))

    def plot_bonds(self, phase):
        from easyCore.Symmetry.Bonding import generate_bonds

        bonds = generate_bonds(phase, max_distance=self.max_distance)
        all_atoms = phase.get_orbits(magnetic_only=False)
        all_atoms_r = np.vstack([np.array(all_atoms[key]) for key in all_atoms.keys()])

        # generate all cell translations
        cTr1, cTr2, cTr3 = np.mgrid[0:2, 0:2, 0:2]
        # cell origin translations: Na x Nb x Nc x 1 x 1 x3
        pos = np.stack([cTr1, cTr2, cTr3], axis=0).reshape((3, -1, 1), order='F')
        R1 = (pos + all_atoms_r[bonds.atom1, :].T.reshape((3, -1, 1)).transpose((0, 2, 1))).reshape((3, -1), order='F')
        R2 = (pos + (all_atoms_r[bonds.atom2, :].T + bonds.dl).reshape((3, -1, 1)).transpose((0, 2, 1))).reshape((3, -1), order='F')
        IDX = np.tile(bonds.idx, (pos.shape[1]))
        
        lattice = phase.cell
        pos = []
        radius = 0.05
        colors = []
        for _ in range(int(bonds.nSym)):
            colors.append(generate_new_color(colors, pastel_factor=0.9))

        def rotation_matrix_from_vectors(vec1, vec2):
            """ Find the rotation matrix that aligns vec1 to vec2
            :param vec1: A 3d "source" vector
            :param vec2: A 3d "destination" vector
            :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
            """
            a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
            v = np.cross(a, b)
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            if np.all(kmat == 0):
                return np.eye(3)
            rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
            return rotation_matrix

        for r1, r2, idx in zip(R1.T, R2.T, IDX):
            if np.any(r1 < 0) | np.any(r2 < 0) |\
                    np.any(r1 > 1) | np.any(r2 > 1):
                # In this silly example we only think about extent = [1, 1, 1]
                continue

            sp = lattice.get_cartesian_coords(r1)
            ep = lattice.get_cartesian_coords(r2)
            cp = (ep - sp) / 2
            polyDataSource = vtk.vtkCylinderSource()
            polyDataSource.SetRadius(radius)
            length = np.linalg.norm(ep - sp)
            polyDataSource.SetHeight(length)

            transform = vtk.vtkTransform()
            rot = rotation_matrix_from_vectors([0, 1, 0], cp)
            np.linalg.norm(sp-ep)
            wxyz = np.identity(4)
            wxyz[0:3, 0:3] = rot
            wxyz[0:3, 3] = sp + cp

            m = vtk.vtkMatrix4x4()
            m.DeepCopy(wxyz.ravel())
            transform.SetMatrix(m)
            transformPD = vtk.vtkTransformPolyDataFilter()
            transformPD.SetTransform(transform)
            transformPD.SetInputConnection(polyDataSource.GetOutputPort())

            transform2 = vtk.vtkTransform()
            wxyz2 = np.identity(4)
            wxyz2[0:3, 3] = - lattice.get_cartesian_coords([0.5, 0.5, 0.5])
            m2 = vtk.vtkMatrix4x4()
            m2.DeepCopy(wxyz2.ravel())
            transform2.SetMatrix(m2)
            transformPD2 = vtk.vtkTransformPolyDataFilter()
            transformPD2.SetTransform(transform2)
            transformPD2.SetInputConnection(transformPD.GetOutputPort())

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformPD2.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(*colors[idx])
            pos.append(actor)
        return pos

    def create_lattice2(self, lattice):
        cubeVertices = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
        cubeEdges = np.array([[0, 1], [0, 2], [0, 4], [1, 3], [3, 2], [2, 6], [6, 4], [6, 7], [4, 5], [5, 7], [3, 7], [1, 5]])
        actors = []
        radius = 0.035

        def rotation_matrix_from_vectors(vec1, vec2):
            """ Find the rotation matrix that aligns vec1 to vec2
            :param vec1: A 3d "source" vector
            :param vec2: A 3d "destination" vector
            :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
            """
            a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
            v = np.cross(a, b)
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            if np.all(kmat == 0):
                return np.eye(3)
            rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
            return rotation_matrix

        for edge in cubeEdges:
            s_ind, e_ind = edge
            sp = lattice.get_cartesian_coords(cubeVertices[s_ind])
            ep = lattice.get_cartesian_coords(cubeVertices[e_ind])
            cp = (ep - sp) / 2
            polyDataSource = vtk.vtkCylinderSource()
            polyDataSource.SetRadius(radius)
            length = np.linalg.norm(ep - sp)
            polyDataSource.SetHeight(length)

            transform = vtk.vtkTransform()
            rot = rotation_matrix_from_vectors([0, 1, 0], cp)
            np.linalg.norm(sp-ep)
            wxyz = np.identity(4)
            wxyz[0:3, 0:3] = rot
            wxyz[0:3, 3] = sp + cp
            # wxyz[2, 3] = wxyz[2, 3] + 10
            # transform.Concatenate(*wxyx.reshape(1, -1).tolist())
            m = vtk.vtkMatrix4x4()
            m.DeepCopy(wxyz.ravel())
            transform.SetMatrix(m)
            transformPD = vtk.vtkTransformPolyDataFilter()
            transformPD.SetTransform(transform)
            transformPD.SetInputConnection(polyDataSource.GetOutputPort())

            transform2 = vtk.vtkTransform()
            wxyz2 = np.identity(4)
            wxyz2[0:3, 3] = - lattice.get_cartesian_coords([0.5, 0.5, 0.5])
            m2 = vtk.vtkMatrix4x4()
            m2.DeepCopy(wxyz2.ravel())
            transform2.SetMatrix(m2)
            transformPD2 = vtk.vtkTransformPolyDataFilter()
            transformPD2.SetTransform(transform2)
            transformPD2.SetInputConnection(transformPD.GetOutputPort())

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformPD2.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([0.40, 0.40, 0.40]) # Lattice color

            actors.append(actor)
        return actors

    def create_lattice(self, lattice):
        trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # This will be a property of the lattice.
        lengths = np.array(lattice[0:3])
        trans = trans_matrix * lengths
        # cubeVertices = np.array(np.meshgrid([0, 1], [0, 1], [0, 1])).T.reshape(-1, 3)
        cubeVertices = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]])
        cubeEdges = np.array([[0, 1], [0, 2], [0, 4], [1, 3], [3, 2], [2, 6], [6, 4], [6, 7], [4, 5], [5, 7], [3, 7], [1, 5]])
        actors = []
        radius = 0.05

        def rotation_matrix_from_vectors(vec1, vec2):
            """ Find the rotation matrix that aligns vec1 to vec2
            :param vec1: A 3d "source" vector
            :param vec2: A 3d "destination" vector
            :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
            """
            a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
            v = np.cross(a, b)
            c = np.dot(a, b)
            s = np.linalg.norm(v)
            kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
            if np.all(kmat == 0):
                return np.eye(3)
            rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
            return rotation_matrix

        for edge in cubeEdges:
            s_ind, e_ind = edge
            sp = trans.dot(cubeVertices[s_ind])
            ep = trans.dot(cubeVertices[e_ind])
            cp = (ep - sp) / 2
            polyDataSource = vtk.vtkCylinderSource()
            polyDataSource.SetRadius(radius)
            length = np.linalg.norm(ep - sp)
            polyDataSource.SetHeight(length)

            transform = vtk.vtkTransform()
            rot = rotation_matrix_from_vectors([0, 1, 0], cp)
            np.linalg.norm(sp-ep)
            wxyz = np.identity(4)
            wxyz[0:3, 0:3] = rot
            wxyz[0:3, 3] = sp + cp
            # wxyz[2, 3] = wxyz[2, 3] + 10
            # transform.Concatenate(*wxyx.reshape(1, -1).tolist())
            m = vtk.vtkMatrix4x4()
            m.DeepCopy(wxyz.ravel())
            transform.SetMatrix(m)
            transformPD = vtk.vtkTransformPolyDataFilter()
            transformPD.SetTransform(transform)
            transformPD.SetInputConnection(polyDataSource.GetOutputPort())


            transform2 = vtk.vtkTransform()
            wxyz2 = np.identity(4)
            wxyz2[0:3, 3] = - trans.dot([0.5, 0.5, 0.5])
            m2 = vtk.vtkMatrix4x4()
            m2.DeepCopy(wxyz2.ravel())
            transform2.SetMatrix(m2)
            transformPD2 = vtk.vtkTransformPolyDataFilter()
            transformPD2.SetTransform(transform2)
            transformPD2.SetInputConnection(transformPD.GetOutputPort())

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformPD2.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([0.05, 0.05, 0.05])

            actors.append(actor)
        return actors

    def create_atoms2(self, system):
        atoms = system.all_sites()
        lattice = system.cell
        actors = []
        colors = ["#ff7f50", "#4682b4", "#6b8e23", "#d2691e", "#5f9ea0", "#8fbc8f", "#6495ed"]
        radii = [(0.1 + 0.004*i) * min(lattice.lengths) for i in range(len(colors))]
        res = 50

        for atom_index, atom_name in enumerate(atoms.keys()):
            radius = radii[atom_index]
            color = self.hex_to_rgb(colors[atom_index])
            for atom in atoms[atom_name]:
                polyDataSource = vtk.vtkSphereSource()
                polyDataSource.SetRadius(radius)
                polyDataSource.SetPhiResolution(res)
                polyDataSource.SetThetaResolution(res)
                polyDataSource.SetCenter(*lattice.get_cartesian_coords(atom))

                transform = vtk.vtkTransform()
                wxyz = np.identity(4)
                wxyz[0:3, 3] = - lattice.get_cartesian_coords([0.5, 0.5, 0.5])
                m = vtk.vtkMatrix4x4()
                m.DeepCopy(wxyz.ravel())
                transform.SetMatrix(m)
                transformPD = vtk.vtkTransformPolyDataFilter()
                transformPD.SetTransform(transform)
                transformPD.SetInputConnection(polyDataSource.GetOutputPort())

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputConnection(transformPD.GetOutputPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(color)
                actor.GetProperty().SetAmbient(0.35)
                actor.GetProperty().SetDiffuse(0.55)
                actor.GetProperty().SetSpecular(0.5)
                actor.GetProperty().SetSpecularPower(7.0)
                actors.append(actor)
        return actors

    def create_atoms(self, system):
        atoms = system.atoms
        lattice = system.lattice
        res = 50
        actors = []
        trans_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # This will be a property of the lattice.
        lengths = np.array(lattice[0:3])
        radius = 0.05 * min(lengths)
        trans = trans_matrix * lengths
        for atom in atoms:
            polyDataSource = vtk.vtkSphereSource()
            polyDataSource.SetRadius(radius)
            polyDataSource.SetPhiResolution(res)
            polyDataSource.SetThetaResolution(res)
            polyDataSource.SetCenter(*trans.dot(atom))

            transform = vtk.vtkTransform()
            wxyz = np.identity(4)
            wxyz[0:3, 3] = - trans.dot([0.5, 0.5, 0.5])
            m = vtk.vtkMatrix4x4()
            m.DeepCopy(wxyz.ravel())
            transform.SetMatrix(m)
            transformPD = vtk.vtkTransformPolyDataFilter()
            transformPD.SetTransform(transform)
            transformPD.SetInputConnection(polyDataSource.GetOutputPort())

            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformPD.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor([1, 0, 0])
            actors.append(actor)
        return actors

    @Slot(int, int, int)
    def mousePressEvent(self, button: int, screenX: int, screenY: int):
        qDebug('CanvasHandler::mousePressEvent()')

    @Slot(int, int, int)
    def mouseMoveEvent(self, button: int, screenX: int, screenY: int):
        qDebug('CanvasHandler::mouseMoveEvent()')

    @Slot(int, int, int)
    def mouseReleaseEvent(self, button: int, screenX: int, screenY: int):
        qDebug('CanvasHandler::mouseReleaseEvent()')

    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        rgb = [int(hex[i:i + 2], 16) for i in (0, 2, 4)]
        rgb = [i/255 for i in rgb]
        return rgb

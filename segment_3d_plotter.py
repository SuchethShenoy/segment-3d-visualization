import pyvista as pv
import trimesh
import math
import torch
from cheetah import Segment, Dipole, Quadrupole, BPM, Drift, ParticleBeam

DIPOLE_GLTF_FILE = "../3D_models/chenrans_hat_ares_ea_small_steerer.gltf"
QUADRUPOLE_GLTF_FILE = "../3D_models/chenrans_hat_ares_ea_quadrupole.gltf"

SCALE_FACTOR = 0.25
ROTATION_ANGLE = math.pi / 2
ROTATION_AXIS = [0, 1, 0]


class Segment3DPlotter:
    def __init__(
        self,
        segment,
        scale_factor=SCALE_FACTOR,
        rotation_angle=ROTATION_ANGLE,
        rotation_axis=ROTATION_AXIS,
        plotter=None,
    ):
        """
        Initializes the 3D plotter with a segment object.
        :param segment: The Segment object containing lattice elements (e.g., Dipole, Quadrupole).
        :param scale_factor: Scaling factor for the 3D models.
        :param rotation_angle: Rotation angle in radians for the 3D models.
        :param rotation_axis: Axis of rotation for the 3D models.
        :param plotter: Optional external PyVista plotter instance.
        """
        self.segment = segment
        self.scale_factor = scale_factor
        self.rotation_angle = rotation_angle
        self.rotation_axis = rotation_axis
        self.plotter = plotter or pv.Plotter()
        self.current_position = (
            0.0  # Track current longitudinal position along the segment
        )

    def load_and_transform_mesh(self, filename, translation_vector, color="white"):
        """
        Loads a 3D model from file, applies transformations, and adds it to the plotter.
        :param filename: Path to the 3D model file.
        :param translation_vector: Translation vector to place the model in the correct position.
        :param color: Color of the mesh in the plot.
        """
        scene = trimesh.load(filename)
        rot_matrix = trimesh.transformations.rotation_matrix(
            self.rotation_angle, self.rotation_axis
        )

        for name, mesh in scene.geometry.items():
            # Apply scaling, rotation, and translation
            mesh.apply_scale(self.scale_factor)
            mesh.apply_transform(rot_matrix)
            mesh.apply_translation(translation_vector)

            # Wrap the mesh with PyVista
            pv_mesh = pv.wrap(mesh)

            # Add to the plotter
            self.plotter.add_mesh(pv_mesh, color=color, label=name)

    def plot_dipole(self, element):
        """
        Plots a Dipole in the 3D scene.
        :param element: Dipole element to plot.
        """
        translation_vector = [0, 0.075, self.current_position]
        # Example .gltf file for Dipole, you can replace it with the actual model path
        self.load_and_transform_mesh(DIPOLE_GLTF_FILE, translation_vector, color="red")
        print(f"Plotted Dipole: {element.name} at position {self.current_position}")

    def plot_quadrupole(self, element):
        """
        Plots a Quadrupole in the 3D scene.
        :param element: Quadrupole element to plot.
        """
        translation_vector = [0, 0, self.current_position]
        # Example .gltf file for Quadrupole, you can replace it with the actual model path
        self.load_and_transform_mesh(
            QUADRUPOLE_GLTF_FILE, translation_vector, color="blue"
        )
        print(f"Plotted Quadrupole: {element.name} at position {self.current_position}")

    def plot_segment(self):
        """
        Iterates through the segment and adds each element (Dipole/Quadrupole) to the 3D plot.
        """
        for element in self.segment.elements:
            if isinstance(element, Dipole):
                self.plot_dipole(element)
                self.current_position += float(
                    element.length
                )  # Update position after the dipole
            elif isinstance(element, Quadrupole):
                self.plot_quadrupole(element)
                self.current_position += float(
                    element.length
                )  # Update position after the quadrupole
            else:
                self.current_position += float(
                    element.length
                )  # For Drift/BPM elements, just update position

        # Need to work on plotting the beam better
        incoming_beam = ParticleBeam.from_astra(
            "../cheetah/tests/resources/ACHIP_EA1_2021.1351.001"
        )
        outgoing_beam = self.segment.track(incoming_beam)
        for i in range(10):
            # Beam path visualization
            initial_pos = torch.tensor([incoming_beam.x[i], incoming_beam.y[i], 0])
            final_pos = torch.tensor(
                [outgoing_beam.x[i], outgoing_beam.y[i], self.current_position]
            )
            beam_path = pv.Line(initial_pos, final_pos)
            # Add beam path to the plotter
            self.plotter.add_mesh(
                beam_path, color="green", line_width=3, label="Beam Path"
            )

    def show(self):
        """
        Renders the 3D plot.
        """
        self.plotter.view_zx()
        self.plotter.add_legend()
        self.plotter.show_axes()
        self.plotter.show()


# # Example usage:
# segment = Segment(
#     elements=[
#         Drift(length=torch.tensor(1.0)),
#         BPM(name="BPM1SMATCH"),
#         Dipole(name="DIPOLE1", length=torch.tensor(0.3)),
#         BPM(name="BPM2SMATCH"),
#         Drift(length=torch.tensor(1.0)),
#         BPM(name="BPM3SMATCH"),
#         Quadrupole(name="QUAD1", length=torch.tensor(0.3)),
#         BPM(name="BPM4SMATCH"),
#         Drift(length=torch.tensor(1.0)),
#         BPM(name="BPM5SMATCH"),
#     ]
# )

# segment.QUAD1.tilt = torch.tensor(3.142e-3)
# segment.DIPOLE1.angle = torch.tensor(3.142e-2)

# # Load incoming beam
# incoming_beam = ParticleBeam.from_astra(
#     "../cheetah/tests/resources/ACHIP_EA1_2021.1351.001"
# )
# outgoing_beam = segment.track(incoming_beam)

# plotter = Segment3DPlotter(segment)

# for i in range(10):
#     # Beam path visualization
#     initial_pos = torch.tensor([incoming_beam.x[i], incoming_beam.y[i], 0])
#     final_pos = torch.tensor([outgoing_beam.x[i], outgoing_beam.y[i], 3.6])
#     beam_path = pv.Line(initial_pos, final_pos)
#     # Add beam path to the plotter
#     plotter.plotter.add_mesh(beam_path, color="green", line_width=1, label="Beam Path")

# plotter.plot_segment()
# plotter.show()

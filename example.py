import torch
from segment_3d_plotter import Segment3DPlotter
from cheetah import Segment, Dipole, Quadrupole, BPM, Drift, ParticleBeam


def main():

    segment = Segment(
        elements=[
            Drift(length=torch.tensor(1.0)),
            BPM(name="BPM1SMATCH"),
            Dipole(name="DIPOLE1", length=torch.tensor(0.3)),
            BPM(name="BPM2SMATCH"),
            Drift(length=torch.tensor(1.0)),
            BPM(name="BPM3SMATCH"),
            Quadrupole(name="QUAD1", length=torch.tensor(0.3)),
            BPM(name="BPM4SMATCH"),
            Drift(length=torch.tensor(1.0)),
            BPM(name="BPM5SMATCH"),
        ]
    )

    segment.QUAD1.tilt = torch.tensor(3.142e-3)
    segment.DIPOLE1.angle = torch.tensor(3.142e-2)

    plotter = Segment3DPlotter(segment)

    plotter.plot_segment()
    plotter.show()


if __name__ == "__main__":
    main()

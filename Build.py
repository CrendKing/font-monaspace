import os
import subprocess

from glyphsLib import GSFont

if __name__ == '__main__':
    TRANSFORMATION = (0.9, 0, 0, 1, 0, 0)
    ADVANCE = TRANSFORMATION[0]
    OUTPUT_FILE = 'Monaspace Neon Var My.glyphs'

    font = GSFont('sources/Variable Fonts/Monaspace Neon Var.glyphs')

    new_version_minor = font.versionMinor + 1
    font.customParameters['versionString'] = font.customParameters['versionString'].replace(str(font.versionMinor), str(new_version_minor))
    font.versionMinor = new_version_minor

    width_axis_index = 0
    new_axes = []
    new_instances = []
    new_masters = []

    for i, axis in enumerate(font.axes):
        if axis.name == 'width':
            width_axis_index = i
        else:
            new_axes.append(axis)

    for instance in font.instances:
        if 'Wide' not in instance.name:
            if len(instance.axes) > width_axis_index:
                del instance.axes[width_axis_index]

            new_instances.append(instance)

    for master in font.masters:
        if 'Wide' not in master.name:
            if len(master.axes) > width_axis_index:
                del master.axes[width_axis_index]

            new_masters.append(master)

    font.axes = new_axes
    font.instances = new_instances
    font.masters = new_masters
    remaining_master_ids = {master.id for master in font.masters}

    for glyph in font.glyphs:
        glyph.layers = [layer for layer in glyph.layers if (layer.associatedMasterId or layer.layerId) in remaining_master_ids]

        for layer in glyph.layers:
            layer.width *= ADVANCE

            for path in layer.paths:
                path.applyTransform(TRANSFORMATION)

            for component in layer.components:
                component.applyTransformation(TRANSFORMATION[0], TRANSFORMATION[3])

    font.save(OUTPUT_FILE)

    subprocess.check_call(['gftools', 'builder', 'config.yaml'])
    os.remove('build.ninja')
    os.remove('.ninja_log')
    os.remove(OUTPUT_FILE)

"""Permissions and needs helpers
"""
from flask_principal import Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))
dev_permission = Permission(RoleNeed('admin'), RoleNeed('developer'))
maintainer_permission = Permission(
    RoleNeed('admin'),
    RoleNeed('developer'),
    RoleNeed('maintainer')
)
installer_permission = Permission(
    RoleNeed('admin'),
    RoleNeed('developer'),
    RoleNeed('maintainer'),
    RoleNeed('installer')
)

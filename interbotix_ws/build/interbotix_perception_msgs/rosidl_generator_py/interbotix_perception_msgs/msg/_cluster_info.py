# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interbotix_perception_msgs:msg/ClusterInfo.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ClusterInfo(type):
    """Metaclass of message 'ClusterInfo'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interbotix_perception_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interbotix_perception_msgs.msg.ClusterInfo')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__cluster_info
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__cluster_info
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__cluster_info
            cls._TYPE_SUPPORT = module.type_support_msg__msg__cluster_info
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__cluster_info

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

            from std_msgs.msg import ColorRGBA
            if ColorRGBA.__class__._TYPE_SUPPORT is None:
                ColorRGBA.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ClusterInfo(metaclass=Metaclass_ClusterInfo):
    """Message class 'ClusterInfo'."""

    __slots__ = [
        '_frame_id',
        '_position',
        '_yaw',
        '_color',
        '_min_z_point',
        '_num_points',
    ]

    _fields_and_field_types = {
        'frame_id': 'string',
        'position': 'geometry_msgs/Point',
        'yaw': 'float',
        'color': 'std_msgs/ColorRGBA',
        'min_z_point': 'geometry_msgs/Point',
        'num_points': 'int32',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'ColorRGBA'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.frame_id = kwargs.get('frame_id', str())
        from geometry_msgs.msg import Point
        self.position = kwargs.get('position', Point())
        self.yaw = kwargs.get('yaw', float())
        from std_msgs.msg import ColorRGBA
        self.color = kwargs.get('color', ColorRGBA())
        from geometry_msgs.msg import Point
        self.min_z_point = kwargs.get('min_z_point', Point())
        self.num_points = kwargs.get('num_points', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.frame_id != other.frame_id:
            return False
        if self.position != other.position:
            return False
        if self.yaw != other.yaw:
            return False
        if self.color != other.color:
            return False
        if self.min_z_point != other.min_z_point:
            return False
        if self.num_points != other.num_points:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def frame_id(self):
        """Message field 'frame_id'."""
        return self._frame_id

    @frame_id.setter
    def frame_id(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'frame_id' field must be of type 'str'"
        self._frame_id = value

    @property
    def position(self):
        """Message field 'position'."""
        return self._position

    @position.setter
    def position(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'position' field must be a sub message of type 'Point'"
        self._position = value

    @property
    def yaw(self):
        """Message field 'yaw'."""
        return self._yaw

    @yaw.setter
    def yaw(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'yaw' field must be of type 'float'"
        self._yaw = value

    @property
    def color(self):
        """Message field 'color'."""
        return self._color

    @color.setter
    def color(self, value):
        if __debug__:
            from std_msgs.msg import ColorRGBA
            assert \
                isinstance(value, ColorRGBA), \
                "The 'color' field must be a sub message of type 'ColorRGBA'"
        self._color = value

    @property
    def min_z_point(self):
        """Message field 'min_z_point'."""
        return self._min_z_point

    @min_z_point.setter
    def min_z_point(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'min_z_point' field must be a sub message of type 'Point'"
        self._min_z_point = value

    @property
    def num_points(self):
        """Message field 'num_points'."""
        return self._num_points

    @num_points.setter
    def num_points(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'num_points' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'num_points' field must be an integer in [-2147483648, 2147483647]"
        self._num_points = value

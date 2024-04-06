// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from interbotix_xs_msgs:msg/JointTrajectoryCommand.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "interbotix_xs_msgs/msg/rosidl_typesupport_c__visibility_control.h"
#include "interbotix_xs_msgs/msg/detail/joint_trajectory_command__struct.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace interbotix_xs_msgs
{

namespace msg
{

namespace rosidl_typesupport_c
{

typedef struct _JointTrajectoryCommand_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _JointTrajectoryCommand_type_support_ids_t;

static const _JointTrajectoryCommand_type_support_ids_t _JointTrajectoryCommand_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _JointTrajectoryCommand_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _JointTrajectoryCommand_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _JointTrajectoryCommand_type_support_symbol_names_t _JointTrajectoryCommand_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interbotix_xs_msgs, msg, JointTrajectoryCommand)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, interbotix_xs_msgs, msg, JointTrajectoryCommand)),
  }
};

typedef struct _JointTrajectoryCommand_type_support_data_t
{
  void * data[2];
} _JointTrajectoryCommand_type_support_data_t;

static _JointTrajectoryCommand_type_support_data_t _JointTrajectoryCommand_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _JointTrajectoryCommand_message_typesupport_map = {
  2,
  "interbotix_xs_msgs",
  &_JointTrajectoryCommand_message_typesupport_ids.typesupport_identifier[0],
  &_JointTrajectoryCommand_message_typesupport_symbol_names.symbol_name[0],
  &_JointTrajectoryCommand_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t JointTrajectoryCommand_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_JointTrajectoryCommand_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace msg

}  // namespace interbotix_xs_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_C_EXPORT_interbotix_xs_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, interbotix_xs_msgs, msg, JointTrajectoryCommand)() {
  return &::interbotix_xs_msgs::msg::rosidl_typesupport_c::JointTrajectoryCommand_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interbotix_xs_msgs:srv/TorqueEnable.idl
// generated code does not contain a copyright notice

#ifndef INTERBOTIX_XS_MSGS__SRV__DETAIL__TORQUE_ENABLE__STRUCT_HPP_
#define INTERBOTIX_XS_MSGS__SRV__DETAIL__TORQUE_ENABLE__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Request __attribute__((deprecated))
#else
# define DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Request __declspec(deprecated)
#endif

namespace interbotix_xs_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct TorqueEnable_Request_
{
  using Type = TorqueEnable_Request_<ContainerAllocator>;

  explicit TorqueEnable_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cmd_type = "";
      this->name = "";
      this->enable = false;
    }
  }

  explicit TorqueEnable_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : cmd_type(_alloc),
    name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cmd_type = "";
      this->name = "";
      this->enable = false;
    }
  }

  // field types and members
  using _cmd_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _cmd_type_type cmd_type;
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _enable_type =
    bool;
  _enable_type enable;

  // setters for named parameter idiom
  Type & set__cmd_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->cmd_type = _arg;
    return *this;
  }
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__enable(
    const bool & _arg)
  {
    this->enable = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Request
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Request
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TorqueEnable_Request_ & other) const
  {
    if (this->cmd_type != other.cmd_type) {
      return false;
    }
    if (this->name != other.name) {
      return false;
    }
    if (this->enable != other.enable) {
      return false;
    }
    return true;
  }
  bool operator!=(const TorqueEnable_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TorqueEnable_Request_

// alias to use template instance with default allocator
using TorqueEnable_Request =
  interbotix_xs_msgs::srv::TorqueEnable_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interbotix_xs_msgs


#ifndef _WIN32
# define DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Response __attribute__((deprecated))
#else
# define DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Response __declspec(deprecated)
#endif

namespace interbotix_xs_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct TorqueEnable_Response_
{
  using Type = TorqueEnable_Response_<ContainerAllocator>;

  explicit TorqueEnable_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit TorqueEnable_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Response
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interbotix_xs_msgs__srv__TorqueEnable_Response
    std::shared_ptr<interbotix_xs_msgs::srv::TorqueEnable_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TorqueEnable_Response_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const TorqueEnable_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TorqueEnable_Response_

// alias to use template instance with default allocator
using TorqueEnable_Response =
  interbotix_xs_msgs::srv::TorqueEnable_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interbotix_xs_msgs

namespace interbotix_xs_msgs
{

namespace srv
{

struct TorqueEnable
{
  using Request = interbotix_xs_msgs::srv::TorqueEnable_Request;
  using Response = interbotix_xs_msgs::srv::TorqueEnable_Response;
};

}  // namespace srv

}  // namespace interbotix_xs_msgs

#endif  // INTERBOTIX_XS_MSGS__SRV__DETAIL__TORQUE_ENABLE__STRUCT_HPP_

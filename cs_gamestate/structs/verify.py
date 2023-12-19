# Verifies an object's attribute being a valid value of the enumerator
def verify_attribute(obj, enum, attr, allow_none=True):
    # The attribute must at least be present
    if not hasattr(obj, attr):
        # Verification failed,return list containing a message explaining the
        # cause:
        return [f"{obj}: Attribute '{attr}' not present"]
    # Get the attribute value out of the object
    #   Note: Might be none
    value = getattr(obj, attr)
    # Optionally allows attributes to be not set
    if allow_none and value is None:
        # Return empty list to be compatible with collecting list of
        # verification messages
        return []
    # Verify by detecting failure of initializing the enum from the attribute
    try:
        # Initialize the enum from the attribute value
        enum(value)
    # Failing to initialize the enum from the attribute value will be signaled
    # by raising a ValueError
    except ValueError:
        # Verification failed, return list containing a message explaining the
        # cause:
        return [f"{obj}: '{attr}': '{value}' not in {[x.value for x in enum]}"]
    # Return empty list to be compatible with collecting list of verification
    # messages
    return []


# Base class to be inherited from to enable automated verification of
# substructures which provide the "verify" method
class VerifiedSubstructures:
    # Tries to verify the validity of the component producing a list of messages
    # if something is not right
    def verify(self):
        # Start collecting messages in list
        messages = []
        # Automate the verification of all substructures
        for attr in self.__dict__:
            # If the attribute has a verify method, this substructure needs to
            # be verified
            if hasattr(self.__dict__[attr], "verify"):
                # Verify the substructure using its method and collecting the
                # messages
                messages.extend(
                    [f"{attr}: {msg}" for msg in getattr(self, attr).verify()]
                )
        # Return the collected verification messages
        return messages

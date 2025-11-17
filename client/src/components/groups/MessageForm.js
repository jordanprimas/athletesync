import { useState, useEffect, useContext } from "react";
import { useFormik } from "formik"
import { UserContext } from "../../contexts/UserContext"
import * as yup from "yup"

/**
Join/leave group logic
TAKE OUT MESSAGE VALUES AND MOVE TO GROUPDETAIL OR CREATE JOIN GROUP COMPONENT
 */


const MessageForm = ({ groupId, updateGroup, userGroups, deleteUserGroup }) => {
  // --- State and Context --- 
  const [errorMessage, setErrorMessage] = useState(null);
  const [joinGroup, setJoinGroup] = useState(false);
  const [user, setUser] = useContext(UserContext);

  // Check if the user is already a member 
  const userJoinedGroup = userGroups.find(userGroup => userGroup.user_id === user.id);
  const userGroupId = userJoinedGroup ? userJoinedGroup.id : null;
  console.log(userGroupId)

  // Keep join state synced with current userGroups  
  useEffect(() => {
    if (userJoinedGroup) {
      setJoinGroup(true)
    } else {
      setJoinGroup(false)
    }
  }, [userGroups, user.id])

  // Validation schema for the message
  const formSchema = yup.object().shape({
    message: yup.string().max(100, "Message cannot exceed 100 characters.")
  })

  const formik = useFormik({ initialValues: { message: "" }, validationSchema: formSchema})

  // Handle join/leave click 
  const handleClick = () => {
    if (!joinGroup) {

      // Validate before sending join request
      if (!formik.isValid) {
        setErrorMessage("Please review errors before joining.");
        return;
      }

      fetch("/api/user_groups", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: formik.values.message,
          group_id: groupId,
        }),
      })
        .then((res) => {
          if (res.ok) return res.json();
          return res.json().then(err => {
            throw new Error(err.error || "Failed to join group");
        });
      })
      .then(data => {
        updateGroup(data);
        setJoinGroup(true);      
        formik.resetForm();       
        setErrorMessage("");      
      })
      .catch((err) => {
        // Display backend error
        setErrorMessage(err.message);
      });   
          
    } else {
      // --- Leave Group Logic --- 

      if (!userGroupId) {
        setErrorMessage("Group not found");
        
      }

      fetch(`/api/user_groups/${userGroupId}`, {
          method: "DELETE",
        })
        .then((res) => {
          if (res.ok) return res.json();
          // Handle failed deletion
          throw new Error("Failed to leave group");
        })
        .then(() => {
          // Update UI state after leaving
          deleteUserGroup(userJoinedGroup);
          setJoinGroup(false);
        })
        .catch((err) => {
          // Display errors if leaving failed
          setErrorMessage(err.message);
        });
    }
  };

  

  return (
    <div className="flex flex-col items-center text-red-400 bg-[#3D7E9F]/10 p-4 rounded-xl shadow-sm space-y-3">
      {/* Error messages */}
      {errorMessage && (
        <p className="text-red-400 text-sm font-medium">{errorMessage}</p>
      )}
      {formik.errors && 
        Object.values(formik.errors).map((error, i) => (
          <p key={i} className="text-red-400 text-sm font-medium">
            {error}
          </p>
        ))}

      {/* Join / Leave Button */}
      <button 
        onClick={handleClick}
        type="button"
        className={`px-4 py-2 rounded-lg font-semibold text-white transition-colors duration-200
          ${joinGroup
            ? 'bg-[#FA8072] hover:bg-[#f56b5a]'
            : 'bg-[#3D7E9F] hover:bg-[#31677c]'
          }`}
      >
        {joinGroup ? "Leave Group" : "Join Group"}
      </button>

      {/* Message input */}
      {!joinGroup && (
        <div>
          <textarea
            type="text"
            name="message"
            value={formik.values.message}
            placeholder="Enter message for the group..."
            onChange={(e) => {
              formik.handleChange(e)
              if (errorMessage) setErrorMessage("") // Clear backend error
            }}
            className="font-mono w-full mt-2 rounded-lg border border-gray-300 px-4 py-2 text-gray-800 text-sm
            h-25 focus outline-none focus:ring-2 focus:ring[#3D7E9F] transition-all resize-y overflow-auto"
          />
        </div>
        )}
    </div>
  )
}

export default MessageForm;

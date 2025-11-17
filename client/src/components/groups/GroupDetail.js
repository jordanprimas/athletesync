import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import MessageForm from "./MessageForm";
import Loading from "../Loading";


const GroupDetail = ({ updateGroup, deleteUserGroup }) => {
  const [openGroupID, setOpenGroupID] = useState(null);
  const { id } = useParams();
  const [group, setGroup] = useState(null);
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/groups/${id}`)
      .then(res => res.json())
      .then(data => {
        setGroup(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching group:", err)
        setLoading(false);
      })
  }, [id]);

  if (loading) return (
    <div className="flex justify-center items-center h-32">
      <div className="w-10 h-10 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
  );

    const toggleGroup = (id) => {
        setOpenGroupID(openGroupID === id ? null : id)
    }


  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Cover Image */}
      <div className="relative h-64 w-full mb-6 rounded-2xl overflow-hidden shadow-lg">
        {group.cover_image ? (
          <img
            src={group.cover_image}
            alt={`${group.name} Cover`}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-[#3D7E9F] to [#86ABBD] flex items-center justify-center text-white text-2xl font-semibold">
            {group.name.charAt(0).toUpperCase()}
          </div>
        )}
     </div>

      {/* Header -Add back button and join group button */}
      {/* If group.user_id === current user show edit group button and delete group button */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold text-[#3D7E9F]">{group.name}</h2>
        {/* <MessageForm groupId={group.id} updateGroup={updateGroup} userGroups={group.user_groups} deleteUserGroup={deleteUserGroup}/> */}
      </div>

       <p className="text-gray-700 mb-8">
          {group.description}
       </p>

      {/* Messages Section  */}
      <p>Discussion</p>
      {/* If message.user_id == current user edit and delete button for message */}

      {/* Member section */}




     
    </div>
  );
};

export default GroupDetail;

 {/* Dropdown Toggle
            <button 
              onClick={() => toggleGroup(group.id)}
              className="flex items-center gap-2 text-sm text-[#3D7E9F] font-medium hover:text-[#86ABBD] transition"
            >
              {openGroupID === group.id ? (
                <>
                  Hide Members <ChevronUp size={16} />
                </>
              ) : (
                <>
                  View Members <ChevronDown size={16} />
                </>
              )}
            </button>

            Members List
            {openGroupID === group.id && (
              <div className="mt-4 bg-gray rounded-lg p-4 border border-gray-200 max-h-60 overflow-y-auto">
                {group.user_groups && group.user_groups.length > 0 ? (
                  <ul className="space-y-2">
                    {group.user_groups.map((userGroup) => (
                      <li
                        key={userGroup.id}
                        className="flex items-start gap-3 bg-white rounded-lg shadow-sm p-3"
                      >
                        - Avatar 
                        <div className="w-8 h-8 rounded-full bg-[#86ABBD] text-white flex items-center justify-center font-semibold">
                            {userGroup.user.username[0].toUpperCase()}
                        </div>

                        - Content
                        <div>
                          <span className="text-gray-800 font-medium">
                            {userGroup.user.username}
                          </span>
                        
                          - Optional message
                          {userGroup.message && (
                            <p className="text-sm text-gray-600">{userGroup.message}</p>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500 text-sm">No members yet</p>
                )}
              </div>


            )} */}

  
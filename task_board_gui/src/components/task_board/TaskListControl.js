import {useEffect, useState} from "react";

const TaskListControl = ({ changeState }) => {
    const [showPopup, setShowPopup] = useState(false);
    const [editMode, setEditMode] = useState(false);
    const [removeMode, setRemoveMode] = useState(false);

    useEffect(() => {
        const callCbAndResetState = () => {
            changeState({
                create_task_flag: showPopup,
                edit_task_flag: editMode,
                remove_task_flag: removeMode
            });
            setShowPopup(false);
            setEditMode(false);
            setRemoveMode(false);
        };

        if (showPopup || editMode || removeMode) {
            callCbAndResetState();
        }
    }, [showPopup, editMode, removeMode, changeState]);

    const handleCreateTask = () => {
        setShowPopup(true);
    };

    const handleEditMode = () => {
        setEditMode(true);
    };

    const handleRemoveMode = () => {
        setRemoveMode(true);
    };

    return (
        <div className="task_list_control">
            <button onClick={handleCreateTask}>Create task</button>
            <button onClick={handleEditMode}>Edit task</button>
            <button onClick={handleRemoveMode}>Remove task</button>
        </div>
    );
};

export default TaskListControl;

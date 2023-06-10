import './styles.css'

const TaskItem = ({task, onTaskClick}) => {

    const handleTaskClick = async () => {
        onTaskClick(task);
    };

    return (
        <li className={"task_item"} onClick={handleTaskClick}>
            <h3 className={"task_title"}>{task.title} {task._id} ({task.due_date})</h3>
            <div className={"members"}>
                <h4 className={"members_header"}>
                    Members
                </h4>
                <ul className={"member_list"}>
                    {task.members_ids.length > 0 ? (
                        <ul className="member_list">
                            {task.members_ids.map((member, index) => (
                                <li key={index} className="member_item">
                                    {member}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <li>No members</li>
                    )}
                </ul>
            </div>
            <div className={"description"}>
                <h4 className={"description_header"}>
                    Description
                </h4>
                <p>
                    {task.description.length >= 20
                        ? `${task.description.slice(0, 20)}...`
                        : task.description.length > 0
                            ? task.description
                            : 'No description'}</p>
            </div>
        </li>
    )
}

export default TaskItem;

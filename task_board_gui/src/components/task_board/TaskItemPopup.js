import './styles.css'

const TaskItemPopup = ({ task }) => {
    return (
        <div className={"task_item"}>
            <h3 className={"task_title"}>Title</h3>
            <input
                id="taskTitle"
                type="text"
                className="task_title_input"
                defaultValue={task.title}
                placeholder={task.title.length > 0 ? '' : 'Enter a title...'}
            />
            <div className={"due_date"}>
                <h4 className={"due_date_header"}>Due date</h4>
                <input
                    id="dueDate"
                    type="text"
                    className="due_date_input"
                    defaultValue={task.due_date}
                    placeholder={task.due_date.length > 0 ? '' : 'Enter a due date...'}
                />
            </div>
            <div className={"members"}>
                <h4 className={"members_header"}>Members</h4>
                <input
                    id="taskMembers"
                    type="text"
                    className="member_input"
                    defaultValue={task.members_ids.length > 0 ? task.members_ids.join(', ') : ''}
                    placeholder={task.members_ids.length > 0 ? '' : 'Enter members...'}
                />
            </div>
            <div className={"description"}>
                <h4 className={"description_header"}>Description</h4>
                <textarea
                    id="taskDescription"
                    className="description_input"
                    defaultValue={task.description.length > 0 ? task.description : ''}
                    placeholder={task.description.length > 0 ? '' : 'Enter description...'}
                />
            </div>
        </div>
    );
};
export default TaskItemPopup;

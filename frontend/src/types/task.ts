export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'review' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  projectId: string;
  assigneeId?: string;
  creatorId: string;
  dueDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskData {
  title: string;
  description: string;
  status?: Task['status'];
  priority?: Task['priority'];
  projectId: string;
  assigneeId?: string;
  dueDate?: string;
}

export interface UpdateTaskData extends Partial<CreateTaskData> {
  id: string;
}

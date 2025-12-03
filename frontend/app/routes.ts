import { layout,route,type RouteConfig } from "@react-router/dev/routes";

export default [
    layout('layout/default.tsx',
    [
        route('/', 'routes/home.tsx'),
        route('/job-boards', 'routes/job_boards.tsx'),
		route('/job-boards/new', 'routes/job_board_new.tsx'),
		route('/job-boards/:jobBoardId/edit', 'routes/job_board_edit.tsx'),
		route('/job-boards/:jobBoardId/delete', 'routes/job_board_delete.tsx'),
        route('/job-boards/:jobBoardId/job-posts', 'routes/job_post.tsx'),
		route('/job-boards/:jobBoardId/post', 'routes/job_post_new.tsx'),
		route("/apply/:postId", "routes/job_application_form.tsx"),
		route("/admin-login","routes/admin_login_form.tsx"),
		route("/admin-logout","routes/admin_logout.tsx"),
		
    ])
]satisfies RouteConfig;
